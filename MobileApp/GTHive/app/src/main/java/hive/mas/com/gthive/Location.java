package hive.mas.com.gthive;

/**
 * Created by bvz on 11/2/15.
 */
public class Location {

    private String mId;
    private String mBId;
    private String mName;
    private int mOccupancy;

    public Location(String id) {
        mId = id;
        mBId = (id.split("-"))[0];
    }

    public Location(String id, String name) {
        mId = id;
        mBId = (id.split("-"))[0];
        mName = name;
    }

    public String getId() {
        return mId;
    }

    public String getBId() {
        return mBId;
    }

    public String getName() {
        return mName;
    }

    public int getOccupancy() {
        return mOccupancy;
    }

    public void setId(String id) {
        mId = id;
    }

    public void setBId(String BId) {
        mBId = BId;
    }

    public void setName(String name) {
        mName = name;
    }

    public void setOccupancy(int occupancy) {
        mOccupancy = occupancy;
    }
}
