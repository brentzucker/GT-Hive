package hive.mas.com.gthive;

import android.content.Context;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;
import android.support.v4.app.FragmentPagerAdapter;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.TextView;

import hive.mas.com.gthive.FavoritesFragment;

/**
 * Created by Stefan on 11/16/15.
 */
//controls views on tabs and which view gets inflated with each tab
public class TabFragmentPagerAdapter extends FragmentPagerAdapter {
    final int PAGE_COUNT = 2;
    private String tabTitles[] = new String[] { "All Buildings", "Favorites" };
    private Context context;

    public TabFragmentPagerAdapter(FragmentManager fm, Context context) {
        super(fm);
        this.context = context;
    }

    @Override
    public int getCount() {
        return PAGE_COUNT;
    }

    @Override
    public Fragment getItem(int position) {
        switch (position) {
            case 0:
                // all buildings fragment activity
                return BuildingListFragment.newInstance(position + 1);
            case 1:
                // favorites list fragment activity
                return FavoritesFragment.newInstance(position + 1);
        }
        return null;
    }

    @Override
    public CharSequence getPageTitle(int position) {
        // Generate title based on item position
        return tabTitles[position];
    }
}
