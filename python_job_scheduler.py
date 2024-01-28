import os
import subprocess
import schedule
import time
import tomllib

from dotenv import load_dotenv


# Function to clone the git repository
def clone_git_repo(repo_url, repo_dir):
    if os.path.exists(repo_dir):
        subprocess.call(["git", "-C", repo_dir, "pull"])
    else:
        subprocess.call(["git", "clone", repo_url, repo_dir])


# Function to install python dependencies
def install_python_dependencies(repo_dir):
    requirements_file = os.path.join(repo_dir, "requirements.txt")
    if os.path.exists(requirements_file):
        subprocess.call(["pip", "install", "-r", requirements_file])


# Function to run python scripts
def run_python_scripts(directory, file):
    subprocess.call(["python", os.path.join(directory, file)])


# Function to load job schedule from config file
def load_job_schedule(config_file):
    with open(config_file, "rb") as file:
        config = tomllib.load(file)
    return config


# Function to schedule jobs
def schedule_jobs(job_schedule, repo_dir):
    for job in job_schedule["scheduled_job"]:
        schedule.every().day.at(job["scheduled_run_time"]).do(
            run_python_scripts, directory=repo_dir, file=job["file"]
        )


# Main function
def main():
    load_dotenv()

    # Get repository URL from environment variable
    repo_url = os.getenv("GIT_REPO_URL")
    if repo_url == None:
        print("Git repo URL not set")
        exit(1)
    repo_dir = "repo"

    # Clone the git repository
    clone_git_repo(repo_url, repo_dir)
    install_python_dependencies(repo_dir)

    # Load job schedule from config file
    config_file = os.path.join(repo_dir, "config.toml")
    job_schedule = load_job_schedule(config_file)

    # Schedule jobs
    schedule_jobs(job_schedule, repo_dir)

    # Run scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
