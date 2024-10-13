import subprocess

command = [
    "python", "-u", "countgd/main_inference.py",
    "--output_dir", "./countgd_test",
    "-c", "config/cfg_fgc1m_test.py",
    "--eval",
    "--datasets", "config/datasets_fgc1m_test.json",
    "--pretrain_model_path", "countgd/checkpoints/checkpoint_fsc147_best.pth",
    "--options", "text_encoder_type=countgd/checkpoints/bert-base-uncased"
]

try:
    # Start the subprocess
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Stream output in real time
    for stdout_line in iter(process.stdout.readline, ""):
        print(stdout_line, end="")  # Print stdout line by line

    # Close the stdout pipe
    process.stdout.close()
    
    # Wait for the process to complete and get the return code
    return_code = process.wait()
    
    if return_code != 0:
        # If there are any errors, print stderr
        stderr_output = process.stderr.read()
        print("Error Output:")
        print(stderr_output)

except Exception as e:
    print(f"An error occurred: {e}")
