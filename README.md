
# VEP Annotation with Docker
Note:This Docker image has been created for research and academic use only.


This guide provides steps to run VEP (Variant Effect Predictor) using a pre-built Docker image. This image includes VEP along with the reference genome, so you can easily annotate your files with a single command.

## Step 1: Pull the Docker Image

Use the following command to pull the Docker image:

```bash
docker pull cosmos9526/vepensemble_with_refgen:latest
```

This image contains VEP with the reference genome ready to use.

## Step 2: Prepare Your Input Directory

Make sure you have a folder containing the input files that you want to process. In this example, we are using the path `/home/ubuntu/00Milad/AUtoWGS_pipeline/input5`. Update the `volume_mapping` variable in the Python code with your directory.

## Step 3: Update the Python Code

Copy the following Python script, which runs VEP using the Docker image:

```python
import subprocess

volume_mapping = "/home/ubuntu/00Milad/AUtoWGS_pipeline/input5:/data"

docker_command = [
    "sudo", "docker", "run", "-it", "--rm", "--user", "root",
    "-v", volume_mapping,
    "cosmos9526/vepensemble_with_refgen:latest",
    "bash", "-c", (
        "vep --fork 12 --offline --host ensembldb.ensembl.org "
        "--buffer_size 100000 --check_existing --everything --allele_number "
        "--total_length --humdiv --no_progress --cache --dir_cache /root/.vep "
        "--species homo_sapiens --assembly GRCh38 "
        "--input_file /data/output.txt "
        "--output_file /data/variantConsensus_VEP.ann.vcf "
        "--force_overwrite --vcf"
    )
]

try:
    subprocess.run(docker_command, check=True)

except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e}")
```

Make sure to change the `volume_mapping` to match your input directory. Once edited, save the file in your directory and run the Python code using Python 3.

## Step 4: Compress VCF File and Index (optional)

To compress your VCF file and create an index for it, use the following commands (after installing bgzip and tabix):

```bash
bgzip NA18564.hard-filtered.chr22.vcf
tabix -p vcf NA18564.hard-filtered.chr22.vcf.gz
```

To test your VCF file, use the following command:

```bash
bcftools query -f '%CHROM\t%POS\t.\t%REF\t%ALT\n' NA18564.hard-filtered.chr22.vcf > output.txt
```

### Installing bgzip, tabix, and bcftools

You can install `bgzip`, `tabix`, and `bcftools` with the following commands:

```bash
sudo apt-get update
sudo apt-get install tabix bcftools
```

Ensure these tools are installed to work with compressed VCF files and for querying VCF data.

## Docker Installation Steps

Before proceeding with the above steps, make sure Docker is installed on your machine. Here's how to install Docker on Ubuntu:

```bash
# Step 1: Update your package list
sudo apt-get update

# Step 2: Install required packages
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common

# Step 3: Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Step 4: Set up the Docker repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Step 5: Update the package database with Docker's packages
sudo apt-get update

# Step 6: Install Docker
sudo apt-get install docker-ce

# Step 7: Verify that Docker is installed
sudo docker --version
```

## Conclusion

By following these steps, you can easily run VEP to annotate your variant files. Adjust the paths according to your input files, and make sure Docker is set up correctly on your system.

## contact info
Milad Bagheri
milad9dxb@gmail.com 




