# Command-line arguments
import argparse
import config

def parse_arguments():
    parser = argparse.ArgumentParser(description='Parsing profiles script')
    parser.add_argument('--id', metavar='id', type=int, nargs='?', help='Profile ID')
    parser.add_argument('--login', metavar='login', type=str, help='LinkedIn login email')
    parser.add_argument('--password', metavar='password', type=str, help='LinkedIn password')
    parser.add_argument('--delay', metavar='delay', type=float, help='Delay between profiles')
    return parser

parser = parse_arguments()

# Parsing command-line arguments
args = parser.parse_args()

# Using arguments in the code
def configure_run():
    id = args.id if args.id is not None else None
    login = args.login if args.login else config.email_linkedin
    password = args.password if args.password else config.password_linkedin
    delay = args.delay if args.delay else 0.4
    return id, login, password, delay

id, login, password, delay = configure_run()
