/*
A basic server implementation
@author Ruiyu Zhang
@created 2019.04.07
@compile JDK11
*/

import java.io.*;
import java.net.Socket;
import java.util.regex.Pattern;

public class Client { // ToDo: dialog interface enhancements
    public static void main(String[] args) {
        if (args == null || args.length != 2) {
            System.err.println(">x> ERROR! Illegal arguments");
            System.exit(100);
        }
        int port = Integer.parseInt(args[1]);
        String commandFormat = "\\b(GET|BOUNCE|EXIT)\\b<.*>|\\bEXIT\\b";

        try {
            /* Initialize */
            Socket socket = new Socket(args[0], port);
            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter out = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()), true);
            BufferedReader userEntry = new BufferedReader(new InputStreamReader(System.in));
            boolean looper = true;

            while (looper) {
                /* Input command */
                System.out.println(">?> Enter command:");
                String command = userEntry.readLine();

                /* Check and send command */
                boolean isLegalInput = command != null && Pattern.matches(commandFormat, command);
                if (isLegalInput) {
                    System.out.println(">>> Command: " + command);
                    out.println(command);
                } else {
                    System.out.println(">!> WARNING: illegal command.");
                    continue;
                }

                /* Receive msg from server */
                System.out.println(">>> SERVER: [" + in.readLine() + "]");

                /* Handle command actions */
                if (command.substring(0, 4).equals("EXIT")) {
                    looper = false;
                } else if (command.substring(0, 3).equals("GET")) {
                    int lines = Integer.parseInt(in.readLine());
                    System.out.println("--START-OF-FILE-----------------------------------------");
                    for (int i = 0; i < lines; i ++) {
                        System.out.println(in.readLine());
                    }
                    System.out.println("--END-OF-FILE-------------------------------------------");
                }
            }
            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
