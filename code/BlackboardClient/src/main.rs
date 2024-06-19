use std::{borrow::Borrow, ops::Range, process::exit};

use api_calls::api_calls::get_ip;
use ::api_calls::api_calls::{
    del_blackboards,
    del_blackboards_specific,
    get_blackboards,
    get_blackboards_status,
    get_blackboards_specific,
    post_blackboards,
    post_blackboards_clear,
    post_blackboards_write,
    set_ip,
};
use colored::Colorize;

use reedline::{
    default_emacs_keybindings,
    ColumnarMenu,
    DefaultCompleter,
    DefaultPrompt,
    Emacs,
    KeyCode,
    KeyModifiers,
    MenuBuilder,
    Reedline,
    ReedlineEvent,
    ReedlineMenu,
    Signal,
};

use regex::Regex;

use clap::Parser;

// helper to get the arguments of a repl command
fn get_args(pat: &str) -> Vec<String> {
    let pattern = r#"(?:\\.|"((?:\\.|[^"\\])*)")|(\S+)|(\s+)"#;
    let re = Regex::new(pattern).unwrap();

    let mut args: Vec<String> = Vec::new();

    for cap in re.captures_iter(pat) {
        if let Some(matched) = cap.get(1) {
            args.push(matched.as_str().replace("\"", ""));
        } else if let Some(matched) = cap.get(2) {
            args.push(matched.as_str().to_string());
        }
    }

    return args;
}

// constants
const DEF_VERSION: u32 = 1;
const DEF_PORT: u32 = 5000;
const DEF_IP: &str = "127.0.0.1";

#[derive(Parser)]
#[command(version, about, long_about = None)]
struct Args {
    #[arg(short, long, default_value_t = DEF_VERSION)]
    api_version: u32,

    #[arg(short, long, default_value_t = DEF_PORT)]
    port: u32,

    #[arg(short, long, default_value_t = DEF_IP.to_string())]
    base: String,
}

fn main() {
    let args = Args::parse();
    set_ip(args.api_version, args.port, args.base.borrow());

    // using continous passing style
    let commands: Vec<String> = vec![
        "clear".to_string(),
        "create".to_string(),
        "delete".to_string(),
        "exit".to_string(),
        "get".to_string(),
        "help".to_string(),
        "list".to_string(),
        "validate".to_string(),
        "write".to_string()
    ];

    // repl setup
    let completer = Box::new(DefaultCompleter::new_with_wordlen(commands.to_vec(), 0));
    let completion_menu = Box::new(ColumnarMenu::default().with_name("completion_menu"));
    let mut keybindings = default_emacs_keybindings();
    keybindings.add_binding(
        KeyModifiers::NONE,
        KeyCode::Tab,
        ReedlineEvent::UntilFound(
            vec![ReedlineEvent::Menu("completion_menu".to_string()), ReedlineEvent::MenuNext]
        )
    );
    let edit_mode = Box::new(Emacs::new(keybindings));
    let mut line_editor = Reedline::create()
        .with_completer(completer)
        .with_menu(ReedlineMenu::EngineCompleter(completion_menu))
        .with_edit_mode(edit_mode);
    let prompt = DefaultPrompt {
        left_prompt: reedline::DefaultPromptSegment::Basic(get_ip().to_string()),
        right_prompt: reedline::DefaultPromptSegment::Empty,
    };

    // repl main loop
    loop {
        let sig = line_editor.read_line(&prompt);
        match sig {
            Ok(Signal::Success(buffer)) => {
                let input = get_args(&buffer);
                let com = input.get(0).unwrap_or(&"help".to_string()).clone();
                let mut args = input.clone();
                if args.len() > 0 {
                    args.remove(0);
                }
                handle_request_command(com, args, &commands);
            }
            Ok(Signal::CtrlD) | Ok(Signal::CtrlC) => {
                println!("\nAborted!");
                break;
            }
            x => {
                println!("Event: {:?}, unknown action", x);
            }
        }
    }
}

//
fn handle_request_command(buffer: String, args: Vec<String>, commands: &Vec<String>) {
    match buffer.as_str() {
        "write" => {
            if check_args(args.clone(), 2..3) {
                let res = post_blackboards_write(args[0].to_string(), args[1].to_string());
                handle_simple_response(res);
            }
        }
        "get" => {
            if check_args(args.clone(), 1..2) {
                let res = get_blackboards_specific(args[0].to_string());
                handle_simple_response(res);
            }
        }
        "create" => {
            if check_args(args.clone(), 2..3) {
                //todo 1 arg
                let res = post_blackboards(
                    args[0].to_string(),
                    args[1].to_string().parse::<u32>().unwrap_or(100)
                );
                handle_simple_response(res);
            }
        }
        "delete" => {
            if check_args(args.clone(), 0..2) {
                let res;
                if args.len() == 1 {
                    res = del_blackboards_specific(args[0].to_string());
                } else {
                    res = del_blackboards();
                }
                handle_simple_response(res);
            }
        }
        "validate" => {
            if check_args(args.clone(), 1..2) {
                let res = get_blackboards_status(args[0].to_string());
                handle_simple_response(res);
            }
        }
        "clear" => {
            if check_args(args.clone(), 1..2) {
                let res = post_blackboards_clear(args[0].to_string());
                handle_simple_response(res);
            }
        }
        "list" => {
            if check_args(args.clone(), 0..1) {
                let res = get_blackboards();
                handle_simple_response(res);
            }
        }
        "help" => {
            println!("Pad all strings that contain whitespaces with double quotes.");
            for name in commands.iter() {
                match name.as_str() {
                    "clear" => println!("Usage: {}. Clear board.", name),
                    "create" =>
                        println!("Usage: {} <name> <duration>. If duration is not parsable, or not given, defaults to 100.", name),
                    "delete" =>
                        println!("Usage: {} (<name>). Delete all boards, or optionally a specified one.", name),
                    "get" => println!("Usage: {} <name>. Get the specified board.", name),
                    "list" => println!("Usage: {}. List all boards.", name),
                    "validate" => println!("Usage: {}. Validate a board.", name),
                    "write" => println!("Usage: {} <name>. Write to the specified board.", name),
                    &_ => println!("Usage: {}", name),
                }
            }
        }
        "exit" => {
            println!("Goodbye");
            exit(0);
        }
        &_ => { println!("{}", "invalid command".red()) }
    }
}

// helpers for argument parsing
fn to_many_args_error() {
    println!("{}", "Too many args".red().bold())
}

fn to_few_args_error() {
    println!("{}", "Expected Argument(s)".red().bold())
}

fn check_args(args: Vec<String>, num_of_accepted_args: Range<usize>) -> bool {
    if args.len() > num_of_accepted_args.clone().max().unwrap() {
        to_many_args_error();
        return false;
    }
    if args.len() < num_of_accepted_args.min().unwrap() {
        to_few_args_error();
        return false;
    }
    return true;
}

// Generic response handler. Since all api calls basicly just print the result, we can just use a generic function to express this. Note that this does NOT take into account the MIME type for printing.
fn handle_simple_response(response: Result<reqwest::blocking::Response, reqwest::Error>) {
    if response.is_err() {
        println!("Connection error occured. Make sure your IP address is correct");
        return;
    }
    let res = response.unwrap();
    let status = res.status();
    let text = res.text().unwrap();
    if status.is_success() {
        println!("{}", text)
    } else {
        println!("{0}: {1}", status.as_str().yellow().italic(), text.white())
    }
}
