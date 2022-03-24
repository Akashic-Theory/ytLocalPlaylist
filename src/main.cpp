//
// Created by Mayank on 3/24/2022.
//

#include "wx/wx.h"
#include "AppFrame.h"

class YTLP : public wxApp {
public:
	bool OnInit() override {
		wxFrame* frame = new AppFrame(nullptr);
		SetTopWindow(frame);
		frame->Show();
		return true;
	}
};

wxIMPLEMENT_APP(YTLP);
