# Unit 2: River Crossing (Vượt Sông)
# Từ điển từ đơn (Words) - Tiếng Anh : Tiếng Việt

unit2_words = {
    # River crossing related
    "Ferry": "Phà/phà nổi",
    "River": "Sông",
    "Crossing": "Vượt/qua",
    "Water obstacle": "Chướng ngại nước",
    "Amphibious": "Lưỡng cư/có khả năng hoạt động trên nước và đất liền",
    
    # Vehicle types
    "Amphibious rig": "Thiết bị lưỡng cư",
    "Ferryboat": "Phà",
    "Transport vehicle": "Phương tiện vận chuyển",
    "Bridge layer": "Máy xếp cầu",
    "Assault boat": "Thuyền tấn công",
    
    # Military engineering
    "Military engineer": "Kỹ sư công binh quân sự",
    "Military engineering": "Công binh quân sự",
    "Cross-country": "Vượt địa hình",
    "All-wheel-drive": "Dẫn động toàn bánh",
    
    # Technical terms
    "Pontoon ferry": "Phà phao",
    "Cable ferry": "Phà dây cáp",
    "Reaction ferry": "Phà phản ứng/phà chuyển hướng",
    "Raft": "Bè/bè gỗ",
    "Barge": "Bè chở hàng",
    
    # Components & specifications
    "Hydraulic": "Thủy lực",
    "Propulsion": "Động lực",
    "Rudder": "Lái",
    "Motor": "Động cơ",
    "Engine": "Động cơ/máy",
    
    "Obstacle": "Chướng ngại",
    "Barrier": "Rào cản",
    "Capacity": "Khả năng",
    "Load": "Tải trọng",
    "Depth": "Độ sâu",
    "Width": "Chiều rộng",
    
    # Structural elements  
    "Cable": "Dây cáp",
    "Chain": "Dây xích",
    "Rope": "Dây neo",
    "Pontoon": "Phao",
    "Deck": "Sàn",
    "Hull": "Thân tàu",
    
    # Operations
    "Deploy": "Triển khai",
    "Lay": "Đặt/xếp",
    "Transport": "Vận chuyển",
    "Connect": "Kết nối",
    "Propel": "Đẩy/chuyển động",
    
    # Military operations
    "Combat": "Chiến đấu",
    "Evacuation": "Sơ tán",
    "Disaster relief": "Cứu trợ thảm họa",
    "Dismounted infantry": "Bộ binh hạ ngựa",
    "Wheeled vehicles": "Phương tiện có bánh xe",
    "Tracked vehicles": "Phương tiện có track/xích",
    
    # Navigation
    "Navigate": "Điều hành",
    "Current": "Dòng chảy",
    "Shore": "Bờ",
    "Bank": "Bờ sông",
    "Waterway": "Đường thủy",
    
    # Safety & design
    "Radiation": "Bức xạ",
    "Protection": "Bảo vệ",
    "Communication": "Liên lạc",
    "Radio": "Vô tuyến",
    "Safe": "An toàn",
}

# Gộp lại để sử dụng cho training
word_dict = unit2_words

# Phiên âm quốc tế (IPA)
unit2_word_ipa = {
    "Ferry": "ˈfɛri",
    "River": "ˈrɪvər",
    "Crossing": "ˈkrɔːsɪŋ",
    "Water obstacle": "ˈwɔːtər ˈɑːbstækəl",
    "Amphibious": "æmˈfɪbiəs",
    "Amphibious rig": "æmˈfɪbiəs rɪɡ",
    "Ferryboat": "ˈfɛriboʊt",
    "Transport vehicle": "ˈtrænspɔːrt ˈviːɪkəl",
    "Bridge layer": "brɪdʒ ˈleɪər",
    "Assault boat": "əˈsɔːlt boʊt",
    "Military engineer": "ˈmɪləteri ɛndʒɪˈnɪr",
    "Military engineering": "ˈmɪləteri ɛndʒɪˈnɪrɪŋ",
    "Cross-country": "krɔːs ˈkʌntri",
    "All-wheel-drive": "ɔːl wil draɪv",
    "Pontoon ferry": "pɑːnˈtuːn ˈfɛri",
    "Cable ferry": "ˈkeɪbəl ˈfɛri",
    "Reaction ferry": "riˈækʃən ˈfɛri",
    "Raft": "ræft",
    "Barge": "bɑːrdʒ",
    "Hydraulic": "haɪˈdrɔːlɪk",
    "Propulsion": "prəˈpʌlʃən",
    "Rudder": "ˈrʌdər",
    "Motor": "ˈmoʊtər",
    "Engine": "ˈɛndʒɪn",
    "Obstacle": "ˈɑːbstækəl",
    "Barrier": "ˈbæriər",
    "Capacity": "kəˈpæsəti",
    "Load": "loʊd",
    "Depth": "dɛpθ",
    "Width": "wɪdθ",
    "Cable": "ˈkeɪbəl",
    "Chain": "tʃeɪn",
    "Rope": "roʊp",
    "Pontoon": "pɑːnˈtuːn",
    "Deck": "dɛk",
    "Hull": "hʌl",
    "Deploy": "dɪˈplɔɪ",
    "Lay": "leɪ",
    "Transport": "ˈtrænspɔːrt",
    "Connect": "kəˈnɛkt",
    "Propel": "prəˈpɛl",
    "Combat": "ˈkɑːmbæt",
    "Evacuation": "ɛvækjuˈeɪʃən",
    "Disaster relief": "dɪˈzæstər rɪˈlif",
    "Dismounted infantry": "dɪsˈmaʊntɪd ˈɪnfəntri",
    "Wheeled vehicles": "wild ˈviːɪkəlz",
    "Tracked vehicles": "trækt ˈviːɪkəlz",
    "Navigate": "ˈnævɪɡeɪt",
    "Current": "ˈkɜːrənt",
    "Shore": "ʃɔːr",
    "Bank": "bæŋk",
    "Waterway": "ˈwɔːtərweɪ",
    "Radiation": "reɪdiˈeɪʃən",
    "Protection": "prəˈtɛkʃən",
    "Communication": "kəmjuːnɪˈkeɪʃən",
    "Radio": "ˈreɪdioʊ",
    "Safe": "seɪf",
}

word_ipa_dict = unit2_word_ipa
