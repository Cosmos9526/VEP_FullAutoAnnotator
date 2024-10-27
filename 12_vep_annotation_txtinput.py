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




# To run this script, first make sure Docker is installed. Then, pull the required Docker image using the following command:
# sudo docker pull cosmos9526/vepensemble_with_refgen:latest
# Next, update the `volume_mapping` variable in the Python script with your input directory:
# volume_mapping = "/path/to/your/input:/data"
# Finally, run the script using the following command:
# python 12_vep_annotation_txtinput.py
