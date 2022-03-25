//
// Created by Mayank on 3/24/2022.
//

#include "AppFrame.h"

AppFrame::AppFrame(wxWindow *parent) : wxFrame(parent, wxID_ANY,_("YouTube Local Playlist Manager"),
											   wxDefaultPosition,wxSize(800, 600),
											   wxDEFAULT_FRAME_STYLE) {
	mgr.SetManagedWindow(this);

	wxMenuBar* menuBar = new wxMenuBar;
	wxMenu* m_file = prepareMenuFile();
	wxMenu* m_help = prepareMenuHelp();

	menuBar->Append(m_file, "&File");
	menuBar->Append(m_help, "&Help");

	SetMenuBar(menuBar);

}

AppFrame::~AppFrame() {
	mgr.UnInit();
}

wxMenu* AppFrame::prepareMenuFile(wxMenuBar* bar) {
	auto* menu = new wxMenu;

	menu->Append(ID_NEW_PLAYLIST, "&New Playlist", "");
	menu->AppendSeparator();
	menu->Append(wxID_EXIT, "E&xit");

	Bind(wxEVT_MENU, [this](wxCommandEvent& WXUNUSED(event)) -> void {
		Close(true);
	}, wxID_EXIT);

	if (bar) {
		bar->Append(menu, "&File");
	}
	return menu;
}

wxMenu* AppFrame::prepareMenuHelp(wxMenuBar* bar) {
	auto* menu = new wxMenu;
	static auto about = wxMessageDialog(this,
	                                    "YouTube Local Playlist Manager\n\n"
	                                    "BUILT - " __DATE__,
	                                    "About YTLP");

	menu->Append(wxID_ABOUT, "&About");

	Bind(wxEVT_MENU, [](wxCommandEvent& WXUNUSED(event)) -> void{
		about.ShowModal();
	}, wxID_ABOUT);

	if (bar) {
		bar->Append(menu, "&Help");
	}
	return menu;
}
