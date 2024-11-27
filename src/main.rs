use std::io::{self, Write};
use std::path::Path;

fn main() {
    println!("where should we create the project?");
    io::stdout().flush().expect("Failed to flush stdout");

    let mut folder = String::new();
    io::stdin()
        .read_line(&mut folder)
        .expect("Failed to read line");
    create_folder(folder);
}

fn create_folder(folder: String) {
    let path = Path::new(folder.trim());
    if path.exists() {
        println!("Folder already exists");
        return;
    }
    match std::fs::create_dir_all(path) {
        Ok(_) => println!("Directory created"),
        Err(e) => println!("Failed to create directory: {}", e),
    }
}
