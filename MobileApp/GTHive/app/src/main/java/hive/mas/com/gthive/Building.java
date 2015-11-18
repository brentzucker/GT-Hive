package hive.mas.com.gthive;

import android.content.Context;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by bvz on 11/1/15.
 */
public class Building extends Location {

    private List<Room> mRooms;
    private List<Floor> mFloors;

    public Building(String id) {
        super(id);
        mRooms = new ArrayList<>();
        mFloors = new ArrayList<>();
    }

    public Building(String id, String name) {
        super(id, name);
        mRooms = new ArrayList<>();
        mFloors = new ArrayList<>();
    }

    public boolean isFavorite(Context context) {

        Favorites favorites = Favorites.get(context);

        return favorites.getBuildingIds().contains(this.getBId());
    }

    // Returns a String of Floor Numbers
    public String getFloorNumbers() {
        String floors = "";
        for (Floor f : getFloors()) {
            floors += f.getFloorNumber() + " ";
        }
        return floors;
    }

    // Returns a String of Room Numbers
    public String getRoomNumbers() {
        String rooms = "";
        for (Room r : getRooms()) {
            rooms += r.getRoomNumber() + " ";
        }
        return rooms;
    }

    /* Accessors and Modifiers */

    public List<Room> getRooms() {
        return mRooms;
    }

    public List<Floor> getFloors() {
        return mFloors;
    }

    public Floor getFloor(char floor) {
        for (Floor f : getFloors()) {
            if (f.getFloorNumber() == floor) {
                return f;
            }
        }
        return null;
    }

    public void setRooms(List<Room> rooms) {
        mRooms = rooms;
    }

    public void setFloors(List<Floor> floors) {
        mFloors = floors;
    }
}
