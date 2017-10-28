package PiHunt2017;

import java.net.HttpURLConnection;
import java.net.URL;

public class URLUtils {

//    public static void main(String s[]) {
//        System.out.println(PiHunt2017.URLUtils.exists("http://www.rgagnon.com/howto.html"));
//        System.out.println(PiHunt2017.URLUtils.exists("http://www.rgagnon.com/pagenotfound.html"));
//    /*
//      output :
//        true
//        false
//    */
//    }

    public static boolean exists(String URLName){
        try {
            HttpURLConnection.setFollowRedirects(false);
            // note : you may also need
            //        HttpURLConnection.setInstanceFollowRedirects(false)
            HttpURLConnection con = (HttpURLConnection) new URL(URLName).openConnection();
            con.setRequestMethod("HEAD");
            return (con.getResponseCode() == HttpURLConnection.HTTP_OK);
        }
        catch (Exception e) {
            e.printStackTrace();
            return false;
        }
    }
}