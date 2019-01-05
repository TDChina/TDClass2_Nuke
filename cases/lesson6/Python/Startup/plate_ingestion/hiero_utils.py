import hiero.ui as hui
import hiero.core as hcore


def get_selection(current_selection):
    selection = []
    for i in current_selection:
        if isinstance(i, hcore.TrackItem) and isinstance(i.parent(), hcore.VideoTrack):
            selection.append(i)
    return selection


def generate_tag(trackitems, seq, shotnum, step):
    if trackitems != []:
        item_count = len(trackitems)
        for count in range(0,item_count):
            i = trackitems[count]
            t = hcore.Tag("shotcode")
            t.setNote("plate #%s#%s#%s" % (seq, str(shotnum).zfill(4), i.parent().name()))
            if len(i.tags()) == 0:
                i.addTag(t)
                if count < item_count-1:
                    if trackitems[count+1].timelineIn() != i.timelineIn():
                        shotnum += step
            else:
                for tag in i.tags():
                    if "plate" in tag.note():
                        tag.setNote("plate #%s#%s#%s" % (seq, str(shotnum).zfill(4), i.parent.name()))
                        if count < item_count:
                            if trackitems[count+1].timelineIn() != i.timelineIn():
                                shotnum += step
        return True
