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
    loop{
        let host = env!("PIXELFLUT_HOST");
        let port = env!("PIXELFLUT_PORT");
        let server = format!("{}:{}", host, port);
        thread::spawn(|| {
            serverconnection(server);
        });
    }




}

fn serverconnection(ip: String) {
    match TcpStream::connect(ip) {
        Ok(mut stream) => {

            let height = 1920;
            let width = 2048;
            let mut rng = thread_rng();
            let mut owned_string: String = format!("\n");
            for n in 0..200{
                let x: u32 = rng.gen_range(0..height);
                let y: u32 = rng.gen_range(0..width);
                let add: u32 = rng.gen_range(1..30);
                let r: u32 = rng.gen_range(0..255);
                let g: u32 = rng.gen_range(0..255);
                let b: u32 = rng.gen_range(0..255);
                let request = format!("PX {} {} {}{}{}\n", x, y, format!("{:X}", r,),format!("{:X}",g),format!("{:X}",b));
                owned_string = [owned_string, request].join("\n");
            }

            write!(stream, "{}", owned_string);

        }Err(e) => {
            println!("Failed to connect: {}", e);
        }
    }
}

