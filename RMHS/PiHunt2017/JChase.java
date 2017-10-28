package PiHunt2017;

import java.util.ArrayList;
import java.util.List;
import java.util.StringJoiner;

import static PiHunt2017.URLUtils.exists;

/**
 * Created by michaelblob on 3/20/17.
 */
public class JChase {
    public static void main(String[] args) {
        List<String> list = new ArrayList<>();
        for (int i = 0; i < 11; i++) {
            int n = i;
            list.addAll(checkList(getList(n)));
        }
        for (String s : list) {
            System.out.print(s + " ");
        }
    }

    private static List<String> getList(int n) {
        List<String> list = new ArrayList<>();
        for (int i = (int) Math.pow(10, n-1); i < Math.pow(10, n); i++) {
            list.add(String.valueOf(i));
        }
        return list;
    }

    private static List<String> checkList(List<String> l) {
        String domain = "http://jchase.com/";
        List<String> positive = new ArrayList<>();
        for (String s : l) {
            System.out.print(s + " " + String.valueOf(exists(domain + s)) + System.lineSeparator());
            if (exists(domain + s)) {
                positive.add(s);
            }
        }
        return positive;
    }
}
