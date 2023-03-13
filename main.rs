use crate::database::Database;
use crate::server::run_server;
use std::thread;
use reqwest::blocking::Client;

mod database;
mod server;

fn main() {
    let db1 = Database::new();
    let db2 = Database::new();
    let db3 = Database::new();

    let port1 = 8000;
    let port2 = 8001;
    let port3 = 8002;

    thread::spawn(move || {
        run_server(port1, db1);
    });

    thread::spawn(move || {
        run_server(port2, db2);
    });

    thread::spawn(move || {
        run_server(port3, db3);
    });

    let mut client = reqwest::blocking::Client::new();

    let response = client.get(&format!("http://localhost:{}/{}", port2, "hello")).send().unwrap();
    assert_eq!(response.status(), reqwest::StatusCode::NOT_FOUND);

    assert_eq!(response.status(), reqwest::StatusCode::OK);

    let response = client.get(&format!("http://localhost:{}/{}", port1, "hello")).send().unwrap();
    assert_eq!(response.status(), reqwest::StatusCode::NOT_FOUND);

    let response = client.get(&format!("http://localhost:{}/{}", port3, "hello")).send().unwrap();
    assert_eq!(response.status(), reqwest::StatusCode::NOT_FOUND);

    let response = client.get(&format!("http://localhost:{}/{}", port2, "hello")).send().unwrap();
    assert_eq!(response.status(), reqwest::StatusCode::OK);
    assert_eq!(response.text().unwrap(), "world");
}
