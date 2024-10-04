#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb

import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    logger.info("Running basic cleaning")

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Getting the raw input data")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    logger.info("Running basic cleaning")
    # Drop outliers
    idx = df["price"].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df["last_review"] = pd.to_datetime(df["last_review"])

    logger.info("Saving locally cleaned data")
    df.to_csv("clean_sample.csv", index=False)

    logger.info("Uploading the cleaned data")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")

    parser.add_argument(
        "--input_artifact", type=str, help="input artifact name", required=True
    )

    parser.add_argument(
        "--output_artifact", type=str, help="output artifact name", required=True
    )

    parser.add_argument(
        "--output_type", type=str, help="output artifact type", required=True
    )

    parser.add_argument(
        "--output_description", type=str, help="Output description", required=True
    )

    parser.add_argument(
        "--min_price", type=float, help="Minimum acceotable price", required=True
    )

    parser.add_argument(
        "--max_price", type=float, help="Maximum acceotable price", required=True
    )

    args = parser.parse_args()

    go(args)
