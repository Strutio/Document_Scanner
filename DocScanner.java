import org.opencv.core.*;
import org.opencv.videoio.VideoCapture;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

import javax.swing.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

// MySQL Database Helper Class
class DatabaseHelper {
    private static final String URL = "your_database_url";  // Replace with your MySQL DB URL
    private static final String USER = "your_username";
    private static final String PASSWORD = "your_password";

    public static Connection connect() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }
}

// Document Scanner Class
public class DocScanner extends JFrame {
    private JLabel imageView;

    public DocScanner() {
        super("Webcam Scanner");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(640, 480);

        imageView = new JLabel();
        add(imageView);

        addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent e) {
                close();
            }
        });

        setVisible(true);
    }

    public void start() {
        VideoCapture videoCapture = new VideoCapture();
        if (!videoCapture.open(0)) {
            System.out.println("Error: Couldn't open webcam!");
            return;
        }

        Mat frame = new Mat();
        while (true) {
            if (videoCapture.read(frame)) {
                processFrame(frame);
                repaint();
            } else {
                System.out.println("Error: Couldn't capture frame!");
                break;
            }
        }

        videoCapture.release();
    }

    private void processFrame(Mat frame) {
        // Convert the frame to grayscale
        Mat grayFrame = new Mat();
        Imgproc.cvtColor(frame, grayFrame, Imgproc.COLOR_BGR2GRAY);

        // Apply Gaussian blur to reduce noise
        Imgproc.GaussianBlur(grayFrame, grayFrame, new Size(5, 5), 0);

        // Edge detection using Canny algorithm
        Mat edged = new Mat();
        Imgproc.Canny(grayFrame, edged, 75, 200);

        // Find contours
        List<MatOfPoint> contours = new ArrayList<>();
        Mat hierarchy = new Mat();
        Imgproc.findContours(edged, contours, hierarchy, Imgproc.RETR_LIST, Imgproc.CHAIN_APPROX_SIMPLE);

        if (!contours.isEmpty()) {
            // Sort contours by area and keep only the largest one
            contours.sort(Comparator.comparingDouble(Imgproc::contourArea));
            Collections.reverse(contours);

            Mat warped = applyPerspectiveTransform(frame, contours);

            // Encode the warped image as a JPEG
            MatOfByte buffer = new MatOfByte();
            Imgcodecs.imencode(".jpg", warped, buffer);

            // Convert encoded image data to byte array and display
            byte[] imageData = buffer.toArray();
            ImageIcon image = new ImageIcon(imageData);
            imageView.setIcon(image);

            // Save the processed image to the database
            saveImageToDatabase(imageData);
        }
    }

    private Mat applyPerspectiveTransform(Mat frame, List<MatOfPoint> contours) {
        MatOfPoint largestContour = contours.get(0);
        MatOfPoint2f contour2f = new MatOfPoint2f(largestContour.toArray());

        // Approximate the contour to a polygon to get the document corners
        MatOfPoint2f approxContour = new MatOfPoint2f();
        double peri = Imgproc.arcLength(contour2f, true);
        Imgproc.approxPolyDP(contour2f, approxContour, 0.02 * peri, true);

        if (approxContour.total() == 4) {
            Point[] points = approxContour.toArray();

            // Sort points in a consistent order (top-left, top-right, bottom-right, bottom-left)
            Point tl = points[0];
            Point tr = points[1];
            Point br = points[2];
            Point bl = points[3];

            // Define the destination points for the bird's-eye view
            Point[] dstPoints = {
                new Point(0, 0),
                new Point(frame.width() - 1, 0),
                new Point(frame.width() - 1, frame.height() - 1),
                new Point(0, frame.height() - 1)
            };

            MatOfPoint2f dst = new MatOfPoint2f(dstPoints);
            Mat transformMatrix = Imgproc.getPerspectiveTransform(approxContour, dst);

            // Apply the perspective transformation
            Mat warped = new Mat();
            Imgproc.warpPerspective(frame, warped, transformMatrix, new Size(frame.width(), frame.height()));

            return warped;
        }

        // If no contour was found or no perspective transformation applied, return the original frame
        return frame;
    }

    private void saveImageToDatabase(byte[] imageData) {
        String sql = "INSERT INTO scanned_documents (image_data) VALUES (?)";

        try (Connection conn = DatabaseHelper.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            
            pstmt.setBytes(1, imageData);
            pstmt.executeUpdate();

            System.out.println("Image saved to database.");
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    private void close() {
        System.out.println("Closing webcam scanner...");
        System.exit(0);
    }

    public static void main(String[] args) {
        System.loadLibrary(Core.NATIVE_LIBRARY_NAME); // Load OpenCV library
        DocScanner scanner = new DocScanner();
        scanner.start();
    }
}
