/*
A basic server implementation
@author Ruiyu Zhang
@created 2019.04.07
@compile JDK11
*/

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;
import java.util.regex.Pattern;

public class Server {
    public static void main(String[] args) {
        if (args == null || args.length != 2) {
            System.err.println(">x> ERROR! Illegal arguments");
            System.exit(100);
        }
        int port = Integer.parseInt(args[1]);
        String commandFormat = "\\b(GET|BOUNCE|EXIT)\\b<.*>|\\bEXIT\\b";

        try {
            ServerSocket serverSocket = new ServerSocket(port);
            boolean flag = true;
            while (flag) {
                // System.out.println(">i> STAND BY: awaiting for connection...");
                try {
                    /* Initialize */
                    Socket socket = serverSocket.accept();
                    BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    PrintWriter out = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()), true);

                    /* Receive command */
                    System.out.print(">?> Enter command:");
                    String command = in.readLine();
                    boolean isLegalInput = command != null && Pattern.matches(commandFormat, command);
                    if (!isLegalInput) {
                        System.out.println(">!> WARNING: illegal command.");
                        out.println(">!> WARNING: illegal command.");
                        continue;
                    }

                    /* Process command */
                    if ("EXIT".equals(command)) {
                        // normal <EXIT>
                        System.out.println(">>> NORMAL EXIT: Ending connection.");
                        out.println(">>> NORMAL EXIT: Ending connection.");
                        flag = false;
                    } else if (command.length() >= 4 && command.substring(0, 4).equals("EXIT")) {
                        // abnormal <EXIT>
                        String exitCode = command.substring(5, command.length() - 1);
                        System.out.println(">>> ABNORMAL EXIT: ending connection. Exit code = " + exitCode);
                        out.println(">>> ABNORMAL EXIT: ending connection. Exit code = " + exitCode);
                        flag = false;
                    } else if (command.substring(0, 6).equals("BOUNCE")) {
                        // <BOUNCE>
                        String clientMsg = command.substring(7, command.length() - 1);
                        System.out.println(">>> BOUNCING client msg: " + clientMsg);
                        out.println(">>> BOUNCING client msg: " + clientMsg);
                    } else if (command.substring(0, 3).equals("GET")) {
                        // <GET>
                        String filename = command.substring(4, command.length() - 1);
                        File file = new File(filename);
                        if (!file.exists()) {
                            System.out.println(">!> GET error: file not found.");
                            out.println(">!> GET error: file not found.");
                        } else {
                            Scanner scanner = new Scanner(file);
                            System.out.println(">>> GET file: " + filename);
                            out.println(">>> GET file: " + filename);
                            // Read file
                            int lines = 0;
                            List<String> content = new LinkedList<>();
                            while (scanner.hasNextLine()) {
                                lines ++;
                                content.add(scanner.nextLine());
                            }
                        }
                    } else {
                        System.out.println(">!> WARNING: illegal command.");
                        out.println(">!> WARNING: illegal command.");
                    }
                    socket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
