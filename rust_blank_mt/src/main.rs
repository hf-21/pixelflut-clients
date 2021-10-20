use std::io::BufReader;
use std::io::prelude::*;
use std::net::TcpStream;
use std::ops::Add;
use std::sync::mpsc;
use std::sync::mpsc::*;
use std::thread;
use std::thread::JoinHandle;
extern crate num_cpus;



fn main() -> std::io::Result<()> {
    let host = env!("PIXELFLUT_HOST");
    let port = env!("PIXELFLUT_PORT");

    let mut stream = TcpStream::connect(format!("{}:{}", host, port))?;
    // stream.set_nonblocking(true);

    let height = 1920;
    let width = 2048;

    let channels: Vec<(Sender<Vec<String>>, Receiver<Vec<String>>)> = (0..num_cpus::get()).map(|_| mpsc::channel()).collect();

    let mut requests: Vec<String> = Vec::new();
    requests.reserve(height);

    for y in 0..height {
        let request = (0..width)
            .map(|x| format!("PX {} {} FFFF00\n", x, y))
            .reduce(|acc, value| acc + value.as_str()).unwrap();


        requests.push(request);
    }

    // for request in requests.iter() {
    //     write!(stream, "{}", request);
    // }

    let chunk_size = requests.len() / channels.len();
    println!("requests: {}, chunk size: {}", requests.len(), chunk_size);

    for (i, (tx, _)) in channels.iter().enumerate() {
        let slice = &mut requests[i*chunk_size..(i+1)*chunk_size];
        tx.send(slice.to_vec());
    }

    let mut threads: Vec<JoinHandle<std::io::Result<()>>> = Vec::new();
    for (tx, mut rx) in channels {
        threads.push(thread::spawn(|| consumer(rx)));
    }

    for thread in threads {
        thread.join();
    }

    println!("{} {}", width, height);

    Ok(())
}

fn consumer(rx: Receiver<Vec<String>>) -> std::io::Result<()> {
    let mut stream = TcpStream::connect("192.168.100.53:8080")?;

    let mut requests = rx.recv().unwrap();

    loop {
        for request in requests.iter() {
            write!(stream, "{}", request);
        }
        match rx.try_recv() {
            Ok(new_requests) => requests = new_requests,
            Err(_) => {},
        }
    }
}
