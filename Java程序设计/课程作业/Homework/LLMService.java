package Class.Homework;

import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class LLMService {
    // 通义 API Key
    private static final String API_KEY = "sk-0678758e3dd1430e898c47d114f56e4e";

    // 阿里云通义兼容模式接口
    private static final String ENDPOINT = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions";

    // 使用的模型：qwen-plus
    private static final String MODEL_NAME = "qwen-plus";

    public String getCodeReview(String javaCode) {
        // 使用 threadId() 方法获取当前线程 ID
        long threadId = Thread.currentThread().threadId();
        System.out.printf("[LLM] [Thread %d] 正在调用大模型\n", threadId); // 加上换行符，便于阅读

        try {
            // 构造发给大模型的Prompt
            // 注意：prompt 中不应包含额外的未转义引号
            String prompt = createSystemPrompt() + "\n\n请审查的代码如下：\n```java\n" + javaCode + "\n```";
            // 构造API请求体
            String jsonPayload = createTongyiPayload(prompt);
            // 发送HTTP POST请求并获得相应
            String responseJson = sendHttpRequest(jsonPayload);
            // 解析相应，提取审查文本
            String reviewResult = parseResponse(responseJson);
            System.out.printf("[LLM] [Thread %d] Tongyiqwen 调用完成\n", threadId);
            return reviewResult;
        } catch (IOException e) {
            return e.getMessage();
        }
    }

    private String createSystemPrompt() {
        return "你是一位专业的Java代码审查工程师。你的任务是审查用户提供的Java代码片段，" +
                "并给该代码片段给出详细的、专业的改进建议。并给出修改后的代码" +
                "请使用Markdown格式返回结果。";
    }

    // 核心修改：确保代码中的所有特殊字符在放入 JSON 字符串前被转义
    private String createTongyiPayload(String prompt) {

        // 1. 系统 Prompt 的内容应该被转义
        String systemPromptEscaped = escapeJsonString(createSystemPrompt());

        // 2. 用户 Prompt 的内容应该被转义
        String userPromptEscaped = escapeJsonString(prompt);

        // 构建 JSON 请求
        return String.format(
                "{\"model\":\"%s\"," +
                        "\"messages\":[" +
                        "{\"role\":\"system\",\"content\":\"%s\"}," +
                        "{\"role\":\"user\",\"content\":\"%s\"}" +
                        "]," +
                        "\"parameters\":{\"temperature\":0.7}" +
                        "}",
                MODEL_NAME,
                systemPromptEscaped,
                userPromptEscaped
        );
    }

    /**
     * 辅助方法：对字符串进行 JSON 转义，处理双引号、反斜杠、换行符等，防止破坏 JSON 结构
     */
    private String escapeJsonString(String value) {
        if (value == null) {
            return "";
        }
        // 注意顺序：先转义反斜杠，再转义双引号和换行符
        return value.replace("\\", "\\\\")  // 转义反斜杠
                .replace("\"", "\\\"")  // 转义双引号
                .replace("\n", "\\n")   // 转义换行符
                .replace("\r", "\\r")   // 转义回车符
                .replace("\t", "\\t");  // 转义 Tab 符
    }

    // 发送HTTP请求
    private String sendHttpRequest(String jsonPayload) throws IOException {
        URL url = new URL(ENDPOINT);
        HttpURLConnection connection = (HttpURLConnection) url.openConnection();
        // 设置请求头
        connection.setRequestMethod("POST");
        connection.setRequestProperty("Content-Type", "application/json");
        connection.setRequestProperty("Authorization", "Bearer " + API_KEY);
        connection.setDoOutput(true);
        // 发送 JSON 数据
        try (OutputStream os = connection.getOutputStream()) {
            byte[] input = jsonPayload.getBytes(StandardCharsets.UTF_8);
            os.write(input, 0, input.length);
        }
        // 读取响应
        int responseCode = connection.getResponseCode();
        // 根据状态码获取输入流
        InputStream is = (responseCode >= 200 && responseCode < 300)
                ? connection.getInputStream()
                : connection.getErrorStream();
        try (BufferedReader br = new BufferedReader(new InputStreamReader(is, StandardCharsets.UTF_8))) {
            StringBuilder response = new StringBuilder();
            String responseLine;
            while ((responseLine = br.readLine()) != null) {
                response.append(responseLine.trim());
            }
            if (responseCode != 200) {
                // 如果 API 返回非 200 状态码，则抛出异常并包含响应内容
                throw new IOException("API 返回错误状态码: " + responseCode + "。响应内容: " + response.toString());
            }
            return response.toString();
        }
    }

    private String parseResponse(String responseJson) throws IOException {
        // 目标：提取 "content":"VALUE" 中的 VALUE
        String contentValue = extractValueFromKey(responseJson, "content");
        if (contentValue != null) {
            // 对提取到的值进行反转义处理 (将 \n 变回换行符，将 \" 变回引号等)
            return contentValue.replace("\\n", "\n")
                    .replace("\\\"", "\"")
                    .replace("\\t", "\t");
        }
        // 提取失败
        throw new IOException("解析失败：未能从 API 响应中找到有效的 'content' 字段。原始响应长度: " + responseJson.length());
    }

    /**
     * 辅助方法：使用正则表达式从 JSON 字符串中提取指定键的值
     * 此版本使用 Pattern.DOTALL 标志，让 '.' 匹配所有字符（包括换行符），
     * 并使用非贪婪匹配 (.*?) 来捕获 content 字段内包含大量转义符的内容。
     */
    private String extractValueFromKey(String jsonString, String key) {
        // 正则表达式: 匹配 "key"\s*:\s*" (捕获组 1: 内容) "
        String regex = "\"" + Pattern.quote(key) + "\"\\s*:\\s*\"(.*?)\"";
        // 编译时使用 Pattern.DOTALL 标志
        Pattern pattern = Pattern.compile(regex, Pattern.DOTALL);
        Matcher matcher = pattern.matcher(jsonString);

        if (matcher.find()) {
            return matcher.group(1); // group(1) 捕获第一个括号内的内容 (即值)
        }
        return null;
    }

    // main 方法保持不变
    public static void main(String[] args) {

    }
}