// 案例 3: Performance Issue Code
public class PerformanceCode {
    // 应该使用 StringBuilder 或 StringBuffer
    public static String concatString(String[] words) {
        String result = "";
        for (String word : words) {
            result = result + word; 
        }
        return result;
    }
}