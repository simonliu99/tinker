package PiHunt2017;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by Simon on 3/20/2017.
 */
public class Contain2or4 {
    public static void main(String[] args) {
        int positive = 0;
        for (int i = 0; i < 1000000; i++) {
            List<Integer> digits = digits(i);
            boolean contains2 = false;
            boolean contains4 = false;
            for (Integer j : digits) {
                if (j == 2) {
                    contains2 = true;
                } else if (j == 4) {
                    contains4 = true;
                }
            }
            if ((contains2&&!contains4)||(!contains2&&contains4)) {
                positive++;
            }
//            System.out.print(i + " " + String.valueOf(contains2) + " " + String.valueOf(contains4) + System.lineSeparator());
        }
        System.out.print(positive);
    }

    static List<Integer> digits(int i) {
        List<Integer> digits = new ArrayList<>();
        while(i > 0) {
            digits.add(i % 10);
            i /= 10;
        }
        return digits;
    }
}
