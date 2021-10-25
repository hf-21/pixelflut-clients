#![feature(iter_zip)]

mod vec2d;
mod client;

use rand::prelude::*;

extern crate rand;

static HEIGHT: usize = 1920;
static WIDTH: usize = 2048;

fn main() -> std::io::Result<()> {

    let color = format!("{:02X?}{:02X?}{:02X?}", (random::<i32>().abs() % 255).clamp(100, 255), (random::<i32>().abs() % 255).clamp(100, 255), (random::<i32>().abs() % 255).clamp(100, 255));
    let mut client = client::Client::init(color.as_str())?;

    client.draw_line(&vec2d::Vec2d {x: 100.0, y: 100.0 }, &vec2d::Vec2d { x: 100.0, y: 300.0 }, None, None);
    client.draw_line(&vec2d::Vec2d {x: 200.0, y: 356.0 }, &vec2d::Vec2d { x: 563.0, y: 50.0 }, None, None);
    client.draw_line(&vec2d::Vec2d {x: 342.0, y: 324.0 }, &vec2d::Vec2d { x: 223.0, y: 655.0 }, None, None);
    client.draw_line(&vec2d::Vec2d {x: 345.0, y: 567.0 }, &vec2d::Vec2d { x: 777.0, y: 425.0 }, None, None);
    client.draw_quad(&vec2d::Vec2d {x: 400.0, y: 500.0 }, 50.0, None);
    client.draw_quad(&vec2d::Vec2d {x: 400.0, y: 500.0 }, 5.0, None);
    client.draw_quad(&vec2d::Vec2d {x: 400.0, y: 500.0 }, 150.0, Some(1.0));
    client.draw_line(&vec2d::Vec2d { x: 1.0, y: 1.0 }, &vec2d::Vec2d { x: 500.0, y: 1.0 }, Some(45.0), Some(&vec2d::Vec2d { x: 250.0, y: 1.0 }));

    client.write_buffer()?;

    Ok(())
}
