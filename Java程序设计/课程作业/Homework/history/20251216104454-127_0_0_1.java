// 案例 1: Buggy Code
public class BuggyCode {
    public static int findMax(int[] arr) {
        if (arr == null || arr.length == 0) {
            return -1;
        }
        int max = arr[0];
        for (int i = 0; i <= arr.length; i++) {
            if (arr[i] > max) {
                max = arr[i];
            }
        }
        return max;
    }
}