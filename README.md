# OpenCV Event Demo

## Getting Started

1. 安装Python（推荐3.10以后的版本）

2. 下载本仓库代码
    ```shell
    git clone https://github.com/RoggeOhta/OpenCV-Event-Demo.git
    cd OpenCV-Event-Demo
    ```
   
3. 安装相关第三方库
   ```shell
   pip install -r reqirements.txt
   ```

4. 运行测试`test6_serial_port.py`获取串口号，并更新config
5. 运行其他测试，根据测试结果微调config配置（详细见docs/doc.md)
6. 运行`main.py`

## Memo

1. 关于测试的详细说明请参考`docs/doc.md`
2. 作为Anchor的Aruco的ID为0，大小为Checker 25mm/Marker 20mm, 且摆放姿态要对准左上角和右上角（具体参考docs中的test2部分）


