import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.core.MatOfByte;
import org.opencv.videoio.VideoCapture;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import javax.swing.*;
import java.awt.*;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

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
    // You can perform any image processing here
    // For simplicity, we'll just convert the frame to grayscale
    Mat grayFrame = new Mat();
    Imgproc.cvtColor(frame, grayFrame, Imgproc.COLOR_BGR2GRAY);

    // Encode the frame as a JPEG image
    MatOfByte buffer = new MatOfByte();
    Imgcodecs.imencode(".jpg", grayFrame, buffer);

    // Convert encoded image data to byte array
    byte[] imageData = buffer.toArray();

    // Display the processed frame
    ImageIcon image = new ImageIcon(imageData);
    imageView.setIcon(image);
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
