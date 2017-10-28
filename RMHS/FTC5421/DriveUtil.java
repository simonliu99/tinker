import java.util.Scanner;

/**
 * Created by michaelblob on 3/14/17.
 */
public class DriveUtil {
    public static void main(String[] args) {
        while (true) {
            Scanner reader = new Scanner(System.in);  // Reading from System.in
            System.out.println("X: ");
            int x = reader.nextInt();
            System.out.println("Y: ");
            int y = reader.nextInt();
            System.out.println("R: ");
            int r = reader.nextInt();
//            double[] polar = cartesianToPolar(x, y);
//            System.out.print(polar[0] + " " + Math.toDegrees(polar[1]) + System.lineSeparator());
            double[] mecanum = mecanumDrive(x, y, 1.0, r, 1.0, 1.0, false);
            System.out.print(mecanum[0] + " " + mecanum[1] + " " + mecanum[2] + " " + mecanum[3] + System.lineSeparator());
        }
    }

    //Return format {r, theta}
    private static double[] cartesianToPolar(double x, double y){
        double r = Math.sqrt(Math.pow(x, 2.0) + Math.pow(y, 2.0));
        double theta = Math.atan2(y, x);
        if (theta < 0) {
            theta += (2 * Math.PI);
        }
        return new double[] {r, theta};
    }

    //    Wheels like
    //    1   2
    //    3   4
    //driveWeight and turnWeight should be in [0,1]
    public static double[] mecanumDrive(double xJoy, double yJoy, double driveWeight, double turnJoy, double turnWeight, double res, boolean resTog){
        double[] polar = cartesianToPolar(xJoy, yJoy);
        double r = polar[0];
        double theta = polar[1];
//        System.out.print(r + " " + Math.toDegrees(theta) + System.lineSeparator());
        double weightedR = driveWeight * r;
        double weightedTurn = turnWeight * turnJoy;
//        System.out.print(weightedR + " " + weightedTurn + System.lineSeparator());

        double v1 = weightedR*Math.sin(theta + (Math.PI/2.0)) + weightedTurn;
        double v2 = weightedR*Math.cos(theta + (Math.PI/2.0)) - weightedTurn;
        double v3 = weightedR*Math.cos(theta + (Math.PI/2.0)) + weightedTurn;
        double v4 = weightedR*Math.sin(theta + (Math.PI/2.0)) - weightedTurn;
//        System.out.print(Math.sin(theta) + " " + Math.toDegrees(theta) + System.lineSeparator());

        double absMaxV =  Math.max(Math.max(Math.max(Math.abs(v1), Math.abs(v2)), Math.abs(v3)), Math.abs(v4));
        if (absMaxV > 1.0) { //max voltage of motors is 1.0, so any values over 1.0 will be scaled down appropriately
            v1 /= absMaxV;
            v2 /= absMaxV;
            v3 /= absMaxV;
            v4 /= absMaxV;
        }
        if (resTog) {
            v1 *= res;
            v2 *= res;
            v3 *= res;
            v4 *= res;
        }
        return new double[] {v1, v2, v3, v4};
    }

}
