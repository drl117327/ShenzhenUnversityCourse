package Class.Homework;

import java.io.*;
import java.net.Socket;
import java.util.Arrays;
import java.util.List;

public class CodeReviewClient {
    private static final String SERVER_IP = "127.0.0.1";
    private static final int SERVER_PORT = 8080;
    private static final String LOG_FILE = "src/Class/Homework/review_log.txt";
    public static void main(String[] args){
        // 若多次运行 先删除原有的文件
        File file = new File(LOG_FILE);
        file.delete();
        // 三个样例
        List<String> testCases = Arrays.asList(
                // 案例 1: 包含常见 bug 的代码片段 (数组越界)
                "// 案例 1: Buggy Code\n" +
                        "public class BuggyCode {\n" +
                        "    public static int findMax(int[] arr) {\n" +
                        "        if (arr == null || arr.length == 0) {\n" +
                        "            return -1;\n" +
                        "        }\n" +
                        "        int max = arr[0];\n" +
                        "        for (int i = 0; i <= arr.length; i++) {\n" +
                        "            if (arr[i] > max) {\n" +
                        "                max = arr[i];\n" +
                        "            }\n" +
                        "        }\n" +
                        "        return max;\n" +
                        "    }\n" +
                        "}",

                // 案例 2: 代码风格不佳的片段
                "// 案例 2: Poor Style Code\n" +
                        "public class StyleCode{public void DoWork(int InputValue){int Result=0;\n" +
                        "if(InputValue>10){Result=InputValue*2;}else{Result=InputValue;}}}",

                // 案例 3: 存在性能隐患的片段 (循环中的 String 拼接)
                "// 案例 3: Performance Issue Code\n" +
                        "public class PerformanceCode {\n" +
                        "    // 应该使用 StringBuilder 或 StringBuffer\n" +
                        "    public static String concatString(String[] words) {\n" +
                        "        String result = \"\";\n" +
                        "        for (String word : words) {\n" +
                        "            result = result + word; \n" +
                        "        }\n" +
                        "        return result;\n" +
                        "    }\n" +
                        "}"
        );

//        // 提交所有测试案例
//        for(int i=0;i<testCases.size();i++){
//            System.out.println("提交第"+(i+1) + "个测试案例");
//            submitCode(testCases.get(i));
//            System.out.println("\n");
//        }

        // **特色功能测试**：并发测试
        System.out.println("并发测试：启动 5 个客户端同时提交：");
        for (int i = 0; i < 5; i++) {
            final int submissionId = i;
            new Thread(() -> {
                // 提交性能隐患的代码片段，模拟多个用户同时提交
                System.out.println("--- 启动并发客户端 #" + submissionId + " ---");
                submitCode(testCases.get(2).replace("PerformanceCode", "PerformanceCode_" + submissionId));
            }).start();
        }
    }

    private static void submitCode(String code){
        try(
            // 建立Socket连接
            Socket socket = new Socket(SERVER_IP, SERVER_PORT);
            // 用于发送数据到服务器
            PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
            // 用于接受服务器数据
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()))
        ){
            // 发送代码片段
            out.println(code);
            // 发送代码结束标志
            out.println("END_OF_CODE");

            // 接受并打印审查报告
            System.out.println("服务器响应");
            String line;
            while((line = in.readLine()) != null && !line.equals("END_OF_REVIEW")){
                System.out.println(line);
            }
        }catch(IOException e){
            System.out.println(e);
        }
    }
}
