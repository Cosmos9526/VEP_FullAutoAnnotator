import os
import subprocess

# Function to run VEP in Docker with a bash -c flag
def run_vep_in_docker(volume_mapping, input_file_name):
    # Define the input and output files
    input_file = f"/data/{input_file_name}"  # Input file path inside the Docker container
    output_file = "/data/variantConsensus_VEP.ann.vcf"  # Changed output file path

    # Build the VEP command to be executed inside the Docker container
    vep_command = (
        f"vep -i {input_file} "
        f"-o {output_file} "
        "--cache "
        "--dir_cache /root/.vep "
        "--assembly GRCh38 "
        "--everything "
        "--force_overwrite "
        "--fork 32 "
        "--buffer_size 9000000 "
        "--symbol "
        "--terms SO "
        "--tsl "
        "--biotype "
        "--hgvs "
        "--vcf "
        "--pick "
        "--transcript_version "
        "--offline "
        "--plugin Frameshift "
        "--plugin Wildtype "
        "--dir_plugins /opt/vep_plugins"
    )

    # Run the Docker container and directly execute the VEP command inside the container with bash -c
    docker_command = [
        "sudo", "docker", "run", "--rm", "--user", "root", 
        "-v", f"{volume_mapping}:/data",  # Attach the specified volume to Docker container as /data
        "cosmos9526/vepensemble_with_refgen:latest"  # Use the Docker image
        , "-c", vep_command  # Execute VEP command inside Docker using bash -c
    ]
    
    # Use subprocess to execute the Docker run command
    subprocess.run(docker_command, check=True)

if __name__ == "__main__":
    # Define volume mapping and input file name as variables
    volume_mapping = "/home/ubuntu/00Milad/AUtoWGS_pipeline/input5"  # Replace with your volume path
    input_file_name = "NA18564.hard-filtered.chr22.vcf"  # Replace with your input file name

    # Run VEP in Docker
    run_vep_in_docker(volume_mapping, input_file_name)
