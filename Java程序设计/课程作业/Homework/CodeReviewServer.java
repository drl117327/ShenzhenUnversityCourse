package Class.Homework;

import java.io.*;
import java.net.*;
import java.sql.SQLOutput;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class CodeReviewServer {
    // 监听端口号
    private static final int PORT = 8080;
    // 使用固定大小的线程池，实现并发处理多个客户端请求
    private final ExecutorService threadPool = Executors.newFixedThreadPool(10);
    private final LLMService llmService = new LLMService(); // 大模型服务

    public static void main(String[] args){
        new CodeReviewServer().start();
    }

    public void start(){
        System.out.println("[Service] 启动代码审查");
        try(ServerSocket serverSocket = new ServerSocket(PORT)){
            System.out.println("[Service] 启动成功，监听端口" + PORT);

            while(true){
                // 1. 接受客户端连接
                Socket clientSocket = serverSocket.accept();
                String clientInfo = clientSocket.getInetAddress().getHostAddress();
                System.out.println("[Server] 收到新的客户端连接：" + clientInfo);
                threadPool.submit(new ClientHandler(clientSocket, llmService));
                if (System.in.available() > 0) {
                    BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
                    String input = reader.readLine();
                    if ("exit".equalsIgnoreCase(input.trim())) {
                        System.out.println("[Server] 正在关闭服务器...");
                        serverSocket.close();
                        threadPool.shutdown();
                        break;
                    }
                }
            }
        }catch(IOException e){
            System.out.println(e);
        }finally{
            System.out.println("[Server] 关闭线程池");
            threadPool.shutdown();
        }
    }
}
