use std::fmt;

#[derive(Clone, Copy)]
pub struct Vec2d {
    pub x: f64,
    pub y: f64,
}

impl Vec2d {
    pub fn interpolate(&self, other: &Vec2d, d: f64) -> Vec2d {
        Vec2d { x: self.x + (other.x - self.x) * d, y: self.y + (other.y - self.y) * d }
    }

    pub fn add_x(&self, x: f64) -> Vec2d {
        Vec2d { x: self.x + x, y: self.y }
    }

    pub fn add_y(&self, y: f64) -> Vec2d {
        Vec2d { x: self.x, y: self.y + y }
    }

    pub fn add(&self, other: &Vec2d) -> Vec2d {
        Vec2d { x: self.x + other.x, y: self.y + other.y }
    }

    pub fn add_scalar(&self, other: f64) -> Vec2d {
        Vec2d { x: self.x + other, y: self.y + other }
    }

    pub fn sub_x(&self, x: f64) -> Vec2d {
        Vec2d { x: self.x - x, y: self.y }
    }

    pub fn sub_y(&self, y: f64) -> Vec2d {
        Vec2d { x: self.x, y: self.y - y }
    }

    pub fn sub(&self, other: &Vec2d) -> Vec2d {
        Vec2d { x: self.x - other.x, y: self.y - other.y }
    }

    pub fn sub_scalar(&self, other: f64) -> Vec2d {
        Vec2d { x: self.x - other, y: self.y - other}
    }

    pub fn rotate_origin(&self, degree: f64) -> Vec2d {
        let degree = degree.to_radians();
        Vec2d {
            x: degree.cos() * self.x - degree.sin() * self.y,
            y: degree.sin() * self.x + degree.cos() * self.y
        }
    }

    pub fn rotate(&self, degree: f64, origin: &Vec2d) -> Vec2d {
        self.sub(origin).rotate_origin(degree).add(origin)
    }

    pub fn ensure_positive(&self) -> Vec2d {
        match self {
            vec if vec.x < 0.0 && vec.y < 0.0 => Vec2d { x: 0.0, y: 0.0 },
            vec if vec.y < 0.0 => Vec2d { x: vec.x, y: 0.0 },
            vec if vec.x < 0.0 => Vec2d { x: 0.0, y: vec.y },
            vec => vec.clone()
        }
    }
}

impl fmt::Display for Vec2d {
    fn fmt(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        write!(formatter, "Vec2d {{ x: {}, y: {} }}", self.x, self.y)
    }
}
