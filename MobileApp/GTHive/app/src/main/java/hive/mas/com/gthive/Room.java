package hive.mas.com.gthive;

/**
 * Created by bvz on 11/2/15.
 */
public class Room extends Location {

    private String mRoomNumber;
    private char mFloorNumber;

    public Room(String id) {
        super(id);

        String[] id_arr = id.split("-");
        mRoomNumber = (id_arr.length > 1 ? id_arr[1] : "null");
        mFloorNumber = mRoomNumber.charAt(0);
    }

    public Room(String id, String name) {
        super(id, name);

        String[] id_arr = id.split("-");
        mRoomNumber = (id_arr.length > 1 ? id_arr[1] : "null");
        mFloorNumber = mRoomNumber.charAt(0);
    }

    /* Accessors and Modifiers */

    public String getRoomNumber() {
        return mRoomNumber;
    }

    public char getFloorNumber() {
        return mFloorNumber;
    }

    public void setRoomNumber(String roomNumber) {
        mRoomNumber = roomNumber;
    }

    public void setFloorNumber(char floorNumber) {
        mFloorNumber = floorNumber;
    }
}
