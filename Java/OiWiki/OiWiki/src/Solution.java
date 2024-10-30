import java.util.List;
import java.util.ArrayList;

class Solution {
    public void dfs(List<String> res, int ind, String curString, int end) {
        if (ind == 0) {
            res.add(curString);
        }
        if (ind == end || curString.charAt(curString.length() - 1) == '1') {
            dfs(res, ind - 1, curString + '1', end);
            dfs(res, ind - 1, curString + '0', end);
        }
        else if(curString.charAt(curString.length() - 1) == '0') {
            dfs(res, ind - 1, curString + '1', end);
        }
    }
    public List<String> validStrings(int n) {
        List<String> ans = new ArrayList<String>();
        String cur="";
        dfs(ans,n,cur,n);
        return ans;
    }
}