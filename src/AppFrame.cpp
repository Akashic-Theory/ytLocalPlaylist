//
// Created by Mayank on 3/24/2022.
//

#include "AppFrame.h"

AppFrame::AppFrame(wxWindow *parent) : wxFrame(parent, -1,_("YouTube Local Playlist Manager"),
											   wxDefaultPosition,wxSize(800, 600),
											   wxDEFAULT_FRAME_STYLE) {
	m_mgr.SetManagedWindow(this);

}

AppFrame::~AppFrame() {
	m_mgr.UnInit();
}
