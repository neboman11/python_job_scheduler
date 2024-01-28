import os
import subprocess
import schedule
import time
import yaml
import glob


# Function to clone the git repository
def clone_git_repo(repo_url, repo_dir):
    if os.path.exists(repo_dir):
        subprocess.call(["git", "-C", repo_dir, "pull"])
    else:
        subprocess.call(["git", "clone", repo_url, repo_dir])


# Function to run python scripts
def run_python_scripts(directory):
    python_files = glob.glob(os.path.join(directory, "*.py"))
    for python_file in python_files:
        subprocess.call(["python", python_file])


# Function to load job schedule from config file
def load_job_schedule(config_file):
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config


# Function to schedule jobs
def schedule_jobs(job_schedule, repo_dir):
    for job in job_schedule:
        schedule.every(job["interval"]).seconds.do(
            run_python_scripts, directory=repo_dir
        )


# Main function
def main():
    # Get repository URL from environment variable
    repo_url = os.getenv("GIT_REPO_URL")
    repo_dir = "repo"

    # Clone the git repository
    clone_git_repo(repo_url, repo_dir)

    # Load job schedule from config file
    config_file = os.path.join(repo_dir, "config.yaml")
    job_schedule = load_job_schedule(config_file)

    # Schedule jobs
    schedule_jobs(job_schedule, repo_dir)

    # Run scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
