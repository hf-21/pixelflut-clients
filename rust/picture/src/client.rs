use crate::vec2d::Vec2d;

use std::net::TcpStream;
use std::io;
use std::io::prelude::*;

pub struct Client {
    stream: TcpStream,
    color: String,
    buffer: String,
}

impl Client {
    pub fn init(color: &str) -> io::Result<Client> {
        let host = format!("{}:{}", env!("PIXELFLUT_HOST"), env!("PIXELFLUT_PORT"));
        Ok(Client { stream: TcpStream::connect(host)?, color: color.to_string(), buffer: String::with_capacity(4096) })
    }

    pub fn draw_line(&mut self, start: &Vec2d, end: &Vec2d, rotation: Option<f64>, rotation_center: Option<&Vec2d>) {
        let mut start= *start;
        let mut end= *end;
        match (rotation, rotation_center) {
            (Some(degree), Some(rotation_center)) => {
                start = start.rotate(degree, rotation_center);
                end = end.rotate(degree, rotation_center);
            },
            (Some(degree), None) => {
                start = start.rotate_origin(degree);
                end = end.rotate_origin(degree);
            },
            _ => {},
        };

        let distance_vec = Vec2d { x: end.x - start.x, y: end.y - start.y };
        let distance = (distance_vec.x.powf(2.0) + distance_vec.y.powf(2.0)).sqrt();

        for step in 1..(distance as i64) {
            let d = (1.0 / (distance)) * step as f64;
            let cur = start.interpolate(&end, d);

            self.execute_command(CommandTypes::Px(cur));
        }
    }

    pub fn draw_quad(&mut self, a: &Vec2d, len: f64, rotation: Option<f64>) {
        let center = a.add_scalar(len / 2.0);
        self.draw_line(a, &a.add_x(len), rotation, Some(&center));
        self.draw_line(a, &a.add_y(len), rotation, Some(&center));
        self.draw_line(&a.add_y(len), &a.add_scalar(len), rotation, Some(&center));
        self.draw_line(&a.add_x(len), &a.add_scalar(len), rotation, Some(&center));
    }

    pub fn draw_circle(&mut self, center: &Vec2d, radius: f64) {
        let mut cur = Vec2d { x: 0.0, y: radius };
        let mut d = 3.0 - 2.0 * radius;

        self._draw_circle(center, &cur);

        while cur.y >= cur.x {
            if d > 0.0 {
                cur = Vec2d { x: cur.x + 1.0, y: cur.y - 1.0 };
                d = d + 4.0 * (cur.x - cur.y) + 10.0;
            }
            else {
                cur = Vec2d { x: cur.x + 1.0, y: cur.y };
                d = d + 4.0 * cur.x + 6.0;
            }

            self._draw_circle(center, &cur);
        }
    }

    fn _draw_circle(&mut self, center: &Vec2d, cur: &Vec2d) {
        self.execute_command(CommandTypes::Px(center.add(cur)));
        self.execute_command(CommandTypes::Px(center.sub(cur)));
        self.execute_command(CommandTypes::Px(Vec2d { x: center.x - cur.x, y: center.y + cur.y }));
        self.execute_command(CommandTypes::Px(Vec2d { x: center.x + cur.x, y: center.y - cur.y }));
        self.execute_command(CommandTypes::Px(Vec2d { x: center.x + cur.y, y: center.y + cur.x }));
        self.execute_command(CommandTypes::Px(Vec2d { x: center.x - cur.y, y: center.y + cur.x }));
        self.execute_command(CommandTypes::Px(Vec2d { x: center.x + cur.y, y: center.y - cur.x }));
        self.execute_command(CommandTypes::Px(Vec2d { x: center.x - cur.y, y: center.y - cur.x }));
    }

    pub fn write_buffer(&mut self) -> io::Result<()> {
        self.stream.write(self.buffer.as_bytes())?;
        self.buffer.clear();
        Ok(())
    }

    fn execute_command(&mut self, command: CommandTypes) {
        let request = match command {
            CommandTypes::Px(vec) => {
                let vec = vec.ensure_positive();
                format!("PX {} {} {}\n", vec.x as i64, vec.y as i64, self.color)
            },
        };
        self.buffer.push_str(request.as_str());
    }
}

enum CommandTypes {
    Px(Vec2d),
}
