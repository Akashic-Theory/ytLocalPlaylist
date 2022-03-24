//
// Created by Mayank on 3/24/2022.
//

#ifndef YTLP_APPFRAME_H
#define YTLP_APPFRAME_H

#include <wx/wx.h>
#include <wx/aui/aui.h>

class AppFrame : public wxFrame {
private:
	wxAuiManager m_mgr;
public:
	AppFrame() = delete;
	AppFrame(AppFrame& other) = delete;
	AppFrame(AppFrame&& other) = delete;
	explicit AppFrame(wxWindow* parent);
	~AppFrame() override;
};


#endif //YTLP_APPFRAME_H
