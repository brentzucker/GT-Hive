package hive.mas.com.gthive;

import java.util.List;

/**
 * Created by bvz on 11/1/15.
 */
public class Building extends Location {

    private List<Room> mRooms;
    private List<Floor> mFloors;

    public Building(String id) {
        super(id);
    }

    public Building(String id, String name) {
        super(id, name);
    }

    /* Accessors and Modifiers */

    public List<Room> getRooms() {
        return mRooms;
    }

    public List<Floor> getFloors() {
        return mFloors;
    }

    public void setRooms(List<Room> rooms) {
        mRooms = rooms;
    }

    public void setFloors(List<Floor> floors) {
        mFloors = floors;
    }
}
