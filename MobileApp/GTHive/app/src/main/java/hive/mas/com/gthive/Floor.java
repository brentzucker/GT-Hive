package hive.mas.com.gthive;

import java.util.List;

/**
 * Created by bvz on 11/2/15.
 */
public class Floor extends Location {

    private char mFloorNumber;
    private List<Room> mRooms;

    public Floor(String id) {
        super(id);
        String[] id_arr = id.split("_");
        mFloorNumber = (id_arr.length > 1 ? id_arr[1].charAt(0) : 'n');
    }

    public Floor(String bId, char floorNumber) {
        super(bId + "_" + floorNumber);
        mFloorNumber = floorNumber;
    }

    /* Accessors and Modifiers */

    public char getFloorNumber() {
        return mFloorNumber;
    }

    public List<Room> getRooms() {
        return mRooms;
    }

    public void setFloorNumber(char floorNumber) {
        mFloorNumber = floorNumber;
    }

    public void setRooms(List<Room> rooms) {
        mRooms = rooms;
    }
}
