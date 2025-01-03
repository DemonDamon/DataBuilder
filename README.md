# DataBuilder 🚀
<div align="center">
<img src="assets/logo1.webp" width="520" alt="ragalaxy logo">
</div>

Welcome to **DataBuilder**! This project leverages the power of large language models to create high-quality, customized datasets for AI training and evaluation. Whether you're building a new AI model or enhancing an existing one, DataBuilder is here to streamline your data preparation process.

![alt text](assets/classdiagram.png)

## Features 🌟

- **Custom Dataset Generation**: Tailor datasets to your specific needs using advanced AI models.
- **High Quality & Diversity**: Ensure your datasets are diverse and representative of real-world scenarios.
- **Scalable Solutions**: Easily scale your dataset generation to meet the demands of any project size.
- **User-Friendly Interface**: Intuitive design makes it easy for anyone to generate datasets, regardless of technical expertise.

## Getting Started 🏁

Follow these steps to get started with DataBuilder:

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DemonDamon/DataBuilder.git
   cd DataBuilder
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your environment:
   - Copy `.env.example` to `.env`
   - Update the `.env` file with your OpenAI API credentials:
   ```plaintext
   OPENAI_API_KEY=your-api-key-here
   OPENAI_API_BASE=https://api.openai.com/v1
   ```

4. Test API Connection:
   ```bash
   python examples/test_api.py
   ```
   If successful, you should see:
   ```
   API 测试成功！
   模型回复: 你好，请问有什么可以帮助您的吗？
   ```

### Usage

1. Interactive Chat Example:
   ```bash
   python examples/chat_completion.py
   ```
   This will start an interactive chat session with GPT-3.5. You can:
   - Type your message and press Enter to chat
   - Type 'clear' to clear chat history
   - Type 'quit' to exit

   Example code:
   ```python
   from dotenv import load_dotenv
   from openai import OpenAI
   import os

   # Load environment variables
   load_dotenv()

   # Configure OpenAI client
   client = OpenAI(
       base_url=os.getenv("OPENAI_API_BASE"),
       api_key=os.getenv("OPENAI_API_KEY")
   )

   messages = []
   print("Welcome to GPT-3.5 Chat! (Type 'quit' to exit, 'clear' to clear history)")

   while True:
       user_input = input("\nYou: ").strip()
       if user_input.lower() == 'quit':
           break
       
       messages.append({"role": "user", "content": user_input})
       print("\nGPT: ", end="", flush=True)
       
       response = client.chat.completions.create(
           model="gpt-3.5-turbo",
           messages=messages,
           stream=True
       )
       
       assistant_message = ""
       for chunk in response:
           if chunk.choices[0].delta.content:
               print(chunk.choices[0].delta.content, end="", flush=True)
               assistant_message += chunk.choices[0].delta.content
       
       if assistant_message:
           messages.append({"role": "assistant", "content": assistant_message})
       print()

2. Generate Data Examples:

    a. Quick Generation [generate_data.py](examples/generate_data.py):

    b. Batch Generation [generate_dataset.py](examples/generate_dataset.py):
    - Uses YAML configuration
    - Supports async processing
    - Handles large-scale generation

    Example configuration [config/default_config.yaml](config/default_config.yaml):

    Run the generator:
    ```bash
    python examples/generate_dataset.py
    ```

    Key differences:
    - `generate_data.py`: Quick testing and small datasets
    - `generate_dataset.py`: Production use with:
        - Configuration management
        - Async processing
        - Batch generation
        - Flexible parameter control

    c. Classification Example [classification.py](examples/classification.py):

    Features:
    - **Automatic Prompt Optimization**: Automatically optimize prompts through multiple training rounds
    - **Accuracy Feedback**: Calculate and display accuracy for each training round
    - **Format Standardization**: Automatically standardize model output formats
    - **Progressive Learning**: Support multi-round iterative training to improve effectiveness

    Run Examples:
    ```bash
    python examples/classification.py
    ```

    Output Example:
    ~~~
    开始第 1 轮训练...
    训练准确率: {'sentiment_accuracy': 0.4}
    新提示词效果更好: 1.0 > 0.4
   
    开始第 2 轮训练...
    训练准确率: {'sentiment_accuracy': 1.0}
   
    开始第 3 轮训练...
    训练准确率: {'sentiment_accuracy': 1.0}
   
    优化后的提示词:
    ```
    对商品评论进行情感分类。
    输入模板: 评论文本: {text}
    输出模板: 情感分类: {sentiment}
    可用标签: {'sentiment': ['正面', '负面', '中性']}
    ```
    ~~~

### Common Issues

1. API Connection Errors:
   - Verify your API key is correct
   - Check if you need to use a proxy (add to `.env`):
     ```plaintext
     OPENAI_PROXY=http://127.0.0.1:7890
     ```
   - Ensure your API base URL is correct

## Contributing 🤝

We welcome contributions from the community! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact 📬

For any questions or feedback, please reach out to us at [bingzhenli@hotmail.com](bingzhenli@hotmail.com).

## Project References 🔍

This project draws inspiration from the [Adala](https://github.com/HumanSignal/Adala) framework, incorporating several key architectural concepts:

### Core Components Inspired by Adala

1. **Agent-Based Architecture**
   - Autonomous data generation agents
   - Iterative learning capabilities
   - Environment-aware processing

2. **Runtime System**
   - Flexible model integration
   - Configurable execution environments
   - Support for multiple LLM providers

3. **Environment Management**
   - Ground truth dataset handling
   - Feedback collection mechanisms
   - Performance metrics tracking

4. **Skills System**
   - Task-specific capabilities
   - Customizable output formats
   - Validation mechanisms

### Key Improvements

We've enhanced several aspects while adapting Adala's concepts:

- **Simplified Configuration**: Streamlined setup process with YAML-based configs
- **Async Processing**: Added robust async support for batch operations
- **Enhanced Validation**: Improved data quality checks and error handling
- **Metrics Collection**: Added comprehensive generation metrics and monitoring

### Future Integrations

Planned features inspired by Adala:
- Memory management for long-term learning
- Advanced feedback collection mechanisms
- Multi-modal data generation support
- Enhanced runtime optimization

For more details about Adala's architecture, see their documentation.

## 🗺 Future Milestones

### 1. Enhanced Agent Architecture
- [ ] Implement teacher-student model architecture (using stronger models to guide weaker ones)
- [ ] Support multiple skill combinations and collaboration
- [ ] Add long-term memory management mechanism
- [ ] Implement asynchronous feedback collection

### 2. Environment System Enhancement
- [ ] Support human-in-the-loop feedback mechanisms
- [ ] Add real-time environment interaction capabilities
- [ ] Implement dynamic dataset management
- [ ] Support incremental learning scenarios

### 3. Runtime Optimization
- [ ] Support multiple LLM providers (e.g., Claude, Wenxin, etc.)
- [ ] Implement automatic model performance evaluation
- [ ] Add model call cost tracking
- [ ] Support batch processing optimization

### 4. Skill System Extension
- [ ] Add Named Entity Recognition (NER) skills
- [ ] Implement multi-task parallel learning
- [ ] Support cross-language skill transfer
- [ ] Add text generation skill templates

### 5. Toolchain Development
- [ ] Provide command-line tools
- [ ] Implement REST API interfaces
- [ ] Support Jupyter Notebook integration
- [ ] Add Web UI interfaces

### 6. Monitoring and Evaluation
- [ ] Implement detailed metrics collection system
- [ ] Add performance visualization panels
- [ ] Support experiment comparison analysis
- [ ] Implement automated testing frameworks

### 7. Multi-modal Support
- [ ] Add image processing capabilities
- [ ] Support speech input and output
- [ ] Implement cross-modal skills
- [ ] Support video content processing