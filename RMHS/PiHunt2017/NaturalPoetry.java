package PiHunt2017;

import java.util.Scanner;

/**
 * Created by michaelblob on 3/22/17.
 */
public class NaturalPoetry {
    public static void main(String[] args) {
        while (true) {
            Scanner reader = new Scanner(System.in);  // Reading from System.in
            System.out.println("A: ");
            int a = reader.nextInt();
            System.out.println("B: ");
            int b = reader.nextInt();
//            String[] list = {"A", "C", "S", "T", "G", "F", "A", "I", "A", "T"};
            String[] list = {"S", "H", "E", "E", "N", "C", "A", "P", "T", "B", "E", "T"};
            int[] ciphered = new int[list.length];
            for (int i = 0; i < list.length; i++) {
                int temp = (int) list[i].charAt(0) - 65;
                ciphered[i] = (temp*a+b)%26;
                System.out.print((char) (ciphered[i]+65) + " ");
            }
            System.out.print(System.lineSeparator());
        }
    }
}
