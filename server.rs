use std::io::{BufReader, BufRead, Write};
use std::net::{TcpListener, TcpStream};
use std::thread;

fn handle_client(mut stream: TcpStream, db: &Database) {
    let mut reader = BufReader::new(&stream);
    let mut request = String::new();

    reader.read_line(&mut request).unwrap();

    let mut parts = request.split_whitespace();
    let method = parts.next().unwrap();
    let path = parts.next().unwrap();
    let _http_version = parts.next().unwrap();

    if method == "GET" {
        let key = &path[1..];
        if let Some(value) = db.get(key) {
            let response = format!("HTTP/1.1 200 OK\r\nContent-Length: {}\r\n\r\n{}\r\n", value.len(), value);
            stream.write(response.as_bytes()).unwrap();
        } else {
            let response = "HTTP/1.1 404 NOT FOUND\r\n\r\n".to_string();
            stream.write(response.as_bytes()).unwrap();
        }
    } else if method == "PUT" {
        let key = &path[1..];
        let mut value = String::new();
        reader.read_line(&mut value).unwrap();
        db.put(key.to_string(), value.trim().to_string());
        let response = "HTTP/1.1 200 OK\r\n\r\n".to_string();
        stream.write(response.as_bytes()).unwrap();
    }
}

fn run_server(port: u16, db: Database) {
    let listener = TcpListener::bind(format!("127.0.0.1:{}", port)).unwrap();
    println!("Listening on port {}", port);

    for stream in listener.incoming() {
        let stream = stream.unwrap();
        let db = db.clone();

        thread::spawn(move || {
            handle_client(stream, &db);
        });
    }
}
