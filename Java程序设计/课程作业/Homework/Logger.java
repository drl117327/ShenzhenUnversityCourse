package Class.Homework;

import java.io.*;
import java.time.*;
import java.time.format.DateTimeFormatter;
/*
* 日志记录模块，写入本地文件(review_log.txt)
*/
public class Logger {
    private static final String LOG_FILE = "src/Class/Homework/review_log.txt";
    private static final DateTimeFormatter FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

    public static synchronized void logActivity(String client, String code, String result){


        try (PrintWriter out = new PrintWriter(new FileWriter(LOG_FILE, true))) {
            out.println("==================================================");
            out.println("时间: " + LocalDateTime.now().format(FORMATTER));
            out.println("客户端: " + client);
            out.println("--- 提交代码 ---");
            out.println(indentCode(code)); // 稍微缩进代码以便阅读
            out.println("--- 审查结果 ---");
            out.println(result.trim());
            out.println("==================================================");
            out.flush();
        } catch (IOException e) {
            System.err.println("[日志] 写入失败: " + e.getMessage());
        }
    }

    // 辅助方法：给代码行添加前缀，方便日志文件阅读
    private static String indentCode(String code) {
        return code.lines()
                .map(line -> "  | " + line)
                .collect(java.util.stream.Collectors.joining("\n"));
    }
}
