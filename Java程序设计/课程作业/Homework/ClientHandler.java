package Class.Homework;

import java.io.*;
import java.net.Socket;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.charset.StandardCharsets;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class ClientHandler implements Runnable{
    private final Socket clientSocket;
    private final LLMService llmService;

    //服务器存储历史记录的根目录
    private static final String HISTORY_DIR = "src/Class/Homework/history";

    public ClientHandler(Socket socket, LLMService llmService){
        this.clientSocket = socket;
        this.llmService = llmService;
        createHistoryDirectory();
    }

    @Override
    public void run(){
        String clientInfo =  clientSocket.getInetAddress().getHostAddress();
        long threadId = Thread.currentThread().threadId();

        try(
            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
        ){
            System.out.printf("[Thread %d] 开始处理来自%s的请求", threadId, clientInfo);
            // 接收代码
            StringBuilder codeBuilder = new StringBuilder();
            String line;
            while((line = in.readLine()) != null && !line.equals("END_OF_CODE")){
                codeBuilder.append(line).append("\n");
            }

            String javaCode = codeBuilder.toString().trim();

            if(javaCode.isEmpty()){
                out.println("error: 未收到代码片段");
                return;
            }

            // 调用LLM
            String reviewResult = llmService.getCodeReview(javaCode);
            saveCodeToFile(javaCode, "127.0.0.1");
            // 记录日志
            Logger.logActivity(clientInfo, javaCode, reviewResult);

            // 结果返回客户端
            out.println("代码审查结果");
            out.println(reviewResult);
            out.println("END_OF_REVIEW");

            System.out.printf("[Thread %d] 请求处理完毕，结果发送给%s", threadId, clientInfo);
        }catch(IOException e){
            System.out.println(e);
        }finally{
            try{
                if(!clientSocket.isClosed()){
                    clientSocket.close();
                }
            }catch(IOException e){

            }
        }
    }

    private void createHistoryDirectory(){
        try{
            Files.createDirectories(Paths.get(HISTORY_DIR));
            System.out.println("历史记录目录已经存在");
        }catch(IOException e){
            System.err.println(e.getMessage());
        }
    }

    private void saveCodeToFile(String javaCode, String clientIP){
        // 1. 生成时间戳
        LocalDateTime now = LocalDateTime.now();
        // 格式化：YYYYMMDDHHmmss
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyyMMddHHmmss");
        String timestamp = now.format(formatter);

        // 2. 构造文件名
        // 将 IP 地址中的点号替换为下划线，以确保文件名有效
        String safeIP = clientIP.replace('.', '_');
        String fileName = String.format("%s-%s.java", timestamp, safeIP);

        // 3. 构造完整路径
        Path filePath = Paths.get(HISTORY_DIR, fileName);

        System.out.println("正在保存代码到: " + filePath);

        try {
            // 4. 使用 Files.write() 写入文件
            // 参数：Path, 字节数组 (代码字符串转为 UTF-8 字节), 写入模式 (默认是创建新文件)
            Files.write(
                    filePath,
                    javaCode.getBytes(StandardCharsets.UTF_8)
            );
            System.out.println("代码提交历史保存成功: " + fileName);
        } catch (IOException e) {
            System.err.println("保存代码文件失败: " + e.getMessage());
        }
    }
}
