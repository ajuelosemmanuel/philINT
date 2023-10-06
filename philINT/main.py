import argparse
import philINT.classes as cl
import philINT.utils as utils


def main():
    parser = argparse.ArgumentParser(
        prog = "philINT",
        description = "philINT allows to retrieve information from an email address or an username"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-e', '--email', help="Target email address", required=False)
    group.add_argument('-u', '--username', help="Target username", required=False)
    parser.add_argument("-x", "--extract", help="Extracts the raw data to a json file", action = "store_true", dest = "output")
    args = parser.parse_args()
    target_person = cl.Person()
    if args.email is not None:
        if not utils.is_email(args.email):
            print("Email address isn't valid")
            exit(0)
        target_email = cl.Email(email_address = args.email)
        target_email.run_all()
        target_person.fill_from_email(target_email)
        utils.print_results_banner()
        target_email.display()
    else:
        target_username = cl.Username(username = args.username)
        target_username.make_connections()
        target_person.fill_from_username(target_username)
        utils.print_results_banner()
    target_person.display()
    if args.output:
        target_person.export_raw_data()
    else:
        print("-------------------------------------")
        target_person.display_raw_data()