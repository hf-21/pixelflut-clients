use std::io::prelude::*;
use std::net::TcpStream;
use std::sync::mpsc;
use std::sync::mpsc::*;
use std::thread;
use std::thread::JoinHandle;
use std::time;

extern crate num_cpus;

static HEIGHT: usize = 1920;
static WIDTH: usize = 2048;
static WORKERS: usize = 16;
static CHUNK_SIZE: usize = HEIGHT / WORKERS;


fn main() -> std::io::Result<()> {
    let mut requests: Vec<String> = gen_requests("FF00FF".to_string());

    let mut threads: Vec<JoinHandle<std::io::Result<()>>> = Vec::with_capacity(WORKERS);
    let mut senders: Vec<Sender<Vec<String>>> = Vec::with_capacity(WORKERS);

    for i in 0..WORKERS {
        let slice = &requests[i * CHUNK_SIZE..(i + 1) * CHUNK_SIZE];

        let (tx, rx) = mpsc::channel();
        tx.send(slice.to_vec()).unwrap();
        senders.push(tx);

        threads.push(thread::spawn(|| worker(rx)));
    }

    thread::sleep(time::Duration::from_secs(2));
    requests = gen_requests("0000FF".to_string());

    for (i, tx) in senders.iter().enumerate() {
        let slice = &requests[i * CHUNK_SIZE..(i + 1) * CHUNK_SIZE];
        tx.send(slice.to_vec()).unwrap();
    }

    for thread in threads {
        let _ = thread.join().unwrap();
    }

    Ok(())
}

fn worker(rx: Receiver<Vec<String>>) -> std::io::Result<()> {
    let host = env!("PIXELFLUT_HOST");
    let port = env!("PIXELFLUT_PORT");

    let mut stream = TcpStream::connect(format!("{}:{}", host, port))?;
    let mut requests = rx.recv().unwrap();

    loop {
        for request in requests.iter() {
            stream.write(request.as_bytes()).unwrap();
        }

        match rx.try_recv() {
            Ok(new_requests) => requests = new_requests,
            Err(_) => {}
        }
    }
}

fn gen_requests(color: String) -> Vec<String> {
    let mut requests: Vec<String> = Vec::with_capacity(HEIGHT);

    for y in 0..HEIGHT {
        let request = (0..WIDTH)
            .map(|x| format!("PX {} {} {}\n", x, y, color))
            .reduce(|acc, value| acc + value.as_str()).unwrap();

        requests.push(request);
    }
    requests
}
