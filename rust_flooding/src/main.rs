use std::io::BufReader;
use std::io::prelude::*;
use std::net::TcpStream;
use std::ops::Add;
use std::sync::mpsc;
use std::fmt::Display;
use std::sync::mpsc::*;
use std::thread;
use random_color::{Color, Luminosity, RandomColor};
use rand::{thread_rng, Rng};
//use gif::{Frame, Encoder, Repeat};

fn main() {
    println!("Flooding!");
    let host = env!("PIXELFLUT_HOST");
    let port = env!("PIXELFLUT_PORT");
    serverconnection(format!("{}:{}", host, port));


}

fn serverconnection(ip: &str) {
    match TcpStream::connect(ip) {
        Ok(mut stream) => {
            println!("Successfully connected to server in port 3333");

            let height = 1920;
            let width = 2048;
            let mut rng = thread_rng();

            loop{

                let x: u32 = rng.gen_range(0..height);
                let y: u32 = rng.gen_range(0..width);
                let add: u32 = rng.gen_range(1..30);

                let color = RandomColor::new()
                    .seed(42) // Optional
                    .alpha(1.0) // Optional
                    .to_rgb_array();
                let request = format!("PX {} {} {}{}{}\n", x, y, color[0], color[1], color[2]);
                write!(stream, "{}", request).unwrap();
            }
            //loop {
            //}
        }Err(e) => {
            println!("Failed to connect: {}", e);
        }
    }
}

