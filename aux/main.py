def config_parse():
    print("Start Data Fusion CICD")
    parser = argparse.ArgumentParser(description="Script to execute Data Fusion CICD.")

    parser.add_argument(
        "--env",
        type=str,
        default="dev",
        dest="env",
        help="Name of the project for Cloud Data Fusion. Default to: data-tools-developer",
    )
    return parser

def config_dataops_parse(subparsers):
    dataops_parser = subparsers.add_parser("dataops", help="Execute dataops tests")
    dataops_parser.set_defaults(func=dataops_func)


def dataops_func(args):
    cdf_project = args.cdf_project
    pipeline.func_labs_migration_pipeline(
        env
    )


if __name__ == "__main__":
    parser = config_parse()
    subparsers = parser.add_subparsers(
        dest="subparser_name", description="Possible Statements to execute"
    )

    config_dataops_parse(subparsers)

    args = parser.parse_args()
    print("Started args: ", args)
    dataops_func(args)
