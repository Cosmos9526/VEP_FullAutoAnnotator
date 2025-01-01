
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

## Step 3: Use text File as Input

Copy the following Python script, which runs VEP using the Docker image:

```python
import subprocess

volume_mapping = "/home/ubuntu/00Milad/AUtoWGS_pipeline/input5:/data"

docker_command = [
    "sudo", "docker", "run", "-it", "--rm", "--user", "root",
    "-v", volume_mapping,
    "cosmos9526/vepensemble_with_refgen:latest",
     "-c", (
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

Make sure to change the `volume_mapping` to match your input directory.

## You can save the file in your directory and run it using Python 3.

Once you've updated the input directory, run the Python script:

```bash
python 12_vep_annotation_txtinput.py
```

## Step 5: Use VCF File as Input

If you want to use a VCF file as input, you can use the following Python script:

```python
import subprocess

def run_vep_in_docker(volume_mapping, input_file_name):
    input_file = f"/data/{input_file_name}"
    output_file = "/data/variantConsensus_VEP.ann.vcf"

    vep_command = (
        f"vep -i {input_file} "
        f"-o {output_file} "
        "--cache --dir_cache /root/.vep --assembly GRCh38 --everything "
        "--force_overwrite --fork 32 --buffer_size 9000000 "
        "--symbol --terms SO --tsl --biotype --hgvs --vcf --pick "
        "--transcript_version --offline --plugin Frameshift --plugin Wildtype "
        "--dir_plugins /opt/vep_plugins"
    )

    docker_command = [
        "sudo", "docker", "run", "--rm", "--user", "root", 
        "-v", f"{volume_mapping}:/data",
        "cosmos9526/vepensemble_with_refgen:latest", "-c", vep_command
    ]
    
    subprocess.run(docker_command, check=True)

if __name__ == "__main__":
    volume_mapping = "/home/ubuntu/00Milad/AUtoWGS_pipeline/input5"
    input_file_name = "NA18564.hard-filtered.chr22.vcf"
    
    run_vep_in_docker(volume_mapping, input_file_name)
```

## Step 6: Compress VCF File and Index

To compress your VCF file and create an index for it, use the following commands (after installing bgzip and tabix):

```bash
bgzip your_vcf_file.vcf
tabix -p vcf your_vcf_file.vcf.gz
```

### Installing bgzip and tabix

You can install `bgzip` and `tabix` with the following commands:

```bash
sudo apt-get update
sudo apt-get install tabix
```

Ensure these tools are installed to work with compressed VCF files.

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

## Additional Test Commands

If you want to test your VCF file, you can use the following commands:

```bash
bgzip NA18564.hard-filtered.chr22.vcf
tabix -p vcf NA18564.hard-filtered.chr22.vcf.gz

bcftools query -f '%CHROM\t%POS\t.\t%REF\t%ALT\n' NA18564.hard-filtered.chr22.vcf > output.txt
```

### Installing bcftools

You can install `bcftools` along with `tabix` using the following commands:

```bash
sudo apt-get update
sudo apt-get install tabix bcftools
```

## contact info
Milad Bagheri
milad9dxb@gmail.com 




