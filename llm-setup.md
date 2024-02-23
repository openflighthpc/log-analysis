## Mixtral Setup (Ollama and OpenLLM)


### **Mixtral 8x7b with Ollama: Installation and Usage Guide**

This Markdown outlines the steps to install Ollama, acquire the Mixtral 8x7b model, and interact with it via the shell prompt or REST API.

#### **Prerequisites:**
- Python 3.6 or above
- 8-16 CPUs
- 48GB of RAM
- 100 GB of Storage
- CUDA and cuDNN installed (Optional)

#### **Installation:**
- **Install Ollama:**
Follow the instructions on the website: Ollama Installation Instruction 

- **Setup Mixtral:**
    Open a terminal and run the following command:
    ```bash
    ollama pull mixtral
    ```

#### **Shell Prompt Usage:**
- **Run Mixtral:**
    Type the below command to run the model in interactive mode.
    ```bash
    ollama run mixtral
    ```

- **Interact with Mixtral:**
     Type your queries directly at the prompt.
    ```bash
    >>> hi
    Hello! It's your friend Mixtral.
    ```
#### **REST API Usage:**

- **Generate a response:**
    ```bash
    curl http://localhost:11434/api/generate -d '{
        "model": "llama2",
        "prompt": "Why is the sky blue?"
    }'
    ```

- **Chat with Mixtral:**
    ```bash
    curl http://localhost:11434/api/chat -d '{
        "model": "mistral",
        "messages": [
            { "role": "user", "content": "why is the sky blue?" }
        ]
    }'
    ```
    For more information , follow link https://github.com/ollama/ollama

### **Mixtral 8x7b with OpenLLM: Installation and Usage Guide**

This Markdown outlines the steps to install Mixtral 8x7b model using OpenLLM, and interact with it via the shell prompt or REST API.

#### **Prerequisites:**
- Python 3.6 or above
- 8-16 CPUs
- 48GB of RAM
- 300 GB of Storage
- CUDA and cuDNN installed (Optional)

#### **Installation and Setup**

- **Environment Setup**
    Install virtualenv and dependencies
    ```bash
    sudo apt update
    sudo apt install python3.10-venv
    python3 -m venv venv
    source venv/bin/activate
    pip install openllm
    pip install "openllm[vllm]"
    ```


- **Manage storage space (if root disk is less than 250GB)**

    ```bash
    sudo mount --bind /mnt /tmp
    # Update ownership of /tmp:
    sudo chown -R ubuntu:ubuntu /tmp
    ```
    
    Create symlinks for huggingface and bentoml directories
    
    ```bash
    mkdir /tmp/huggingface /tmp/bentoml
    mkdir /home/ubuntu/.cache/huggingface /home/ubuntu/bentoml
    rsync -av /home/ubuntu/.cache/huggingface/ /tmp/huggingface
    rsync -av /home/ubuntu/bentoml/ /tmp/bentoml
    rm -rf /home/ubuntu/.cache/huggingface /home/ubuntu/bentoml
    ln -s /tmp/huggingface /home/ubuntu/.cache/huggingface
    ln -s /tmp/bentoml /home/ubuntu/bentoml
    ```

- **Download Mixtral Model Files**

    Open a Python interpreter:
    ```bash
    (venv)$ python
    ```
    Download model files using hf_hub_download:
    
    ```bash
    import sys
    from huggingface_hub import hf_hub_download
    
    model_files = [
        "config.json",
        "generation_config.json",
        "model.safetensors.index.json",
        "special_tokens_map.json",
        "tokenizer.json",
        "tokenizer.model",
        "tokenizer_config.json",
    ]
    
    for i in range(1, 20):
        model_files.append(f"model-0000{i}-of-00019.safetensors")
    
    for file in model_files:
        hf_hub_download(repo_id="mistralai/Mixtral-8x7B-v0.1", filename=file)
    ```

    Exit the interpreter:
    
    ```bash
    exit()
    ```

#### **Import and Start the Model**

- **Import into BentoML local store:**
    ```bash
    openllm import mistralai/Mixtral-8x7B-v0.1
    ```
    If using VLLM backend:
    ```bash
    openllm import mistralai/Mixtral-8x7B-v0.1 --backend vllm
    ```

- **Start the model:**
    ```bash
    openllm start mistralai/Mixtral-8x7B-v0.1
    ```
    If using VLLM backend:
    ```bash
    openllm start mistralai/Mixtral-8x7B-v0.1 --backend vllm
    ```
    For usage and other details, follow link https://github.com/bentoml/OpenLLM
