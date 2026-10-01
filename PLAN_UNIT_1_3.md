# Kế hoạch tổng kết Oxford Discover 4 — Unit 1–3

Đối tượng cố định: học sinh 9 tuổi, Grade 4 ESL. Bản xem thử đã triển khai tại `index.html`; skill đã thêm review mode. Xem trạng thái kiểm tra thực tế tại [qa/QA_REPORT.md](qa/QA_REPORT.md). Các mục dưới đây giữ kế hoạch và căn cứ khảo sát ban đầu.

## 1. Căn cứ đã kiểm tra

- PDF đầu vào: `778_7-Oxford Discover 4. Teacher's Guide_2019, 2nd, 232p.pdf`, 232 trang, có lớp văn bản; một số ký tự trích xuất bị lỗi nên vẫn cần đối chiếu bản render.
- Scope and Sequence: trang PDF 2–3. Mục lục và các trang mở unit xác nhận phạm vi bài học.
- Unit 1–2: Big Question “Where are we in the universe?”. Unit 3 bắt đầu Big Question “How do we know what happened long ago?” của cặp Unit 3–4. Không đưa nội dung Unit 4 vào tổng kết Unit 3.
- Trang PDF 36 tái hiện Student Book 8–9: 11 từ Unit 1 có ảnh riêng. Trang PDF 56 tái hiện Student Book 28–29: 11 từ Unit 3 có ảnh riêng. Đã kiểm tra trực quan hai trang.
- Trang PDF 44 tái hiện Student Book 16–17: Unit 2 có danh sách 11 từ, ảnh minh họa và sơ đồ, nhưng không có 11 ảnh riêng. Cần khảo sát các trang còn lại để xác định ảnh dùng được cho từng từ.
- Teacher's Guide chứa cả nội dung học sinh, teacher notes và answer keys. Phải phân biệt ba vùng này khi trích nội dung.
- Chưa có nhật ký/ngày học hay sản phẩm HTML đã gen trong thư mục khảo sát. Vì vậy có thể tổng kết theo unit/lesson strand; chưa thể khẳng định em đã học nội dung nào ở từng buổi thực tế.

## 2. Đánh giá skill hiện có

Skill `od4_esl_learning_designer_skill` đã có nền tảng tốt: đối tượng 9 tuổi ESL, bám nguồn, vocab theo nhóm nghĩa, IPA/sound-it-out/audio, mind map, diễn đạt và recall. Giữ các yêu cầu này; tính năng phát âm mới chỉ được mô tả trong skill, chưa có sản phẩm chạy để kiểm tra.

Các thiếu hụt cần sửa:

1. Chưa có chế độ review nhiều unit hoặc tổng kết các buổi đã học; hành trình 10 bước hiện tại dễ biến bài ôn thành bài dạy mới quá dài.
2. Chưa có schema nguồn đến từng mục, phân biệt số trang PDF / Teacher's Guide / Student Book và trạng thái nội dung đã học.
3. Schema vocab có đường dẫn ảnh nhưng chưa lưu trang nguồn, vùng crop, từ tương ứng, chất lượng và trạng thái đối chiếu.
4. Chưa có quy trình trích ảnh có thể chạy lại, kiểm tra ảnh đúng nghĩa, xử lý ảnh dùng chung và thiếu ảnh.
5. Rubric hiện tại chưa kiểm tra đầy đủ ảnh, phạm vi tổng kết và sự khác nhau giữa nhận biết / nhớ lại / dùng được từ.
6. Wonders/CLC không cần cho bản tổng kết mặc định này; chỉ thêm khi có yêu cầu riêng.

Skill `skills/pdf_to_html_ocr_skill` có quy tắc giữ hình nguồn hữu ích nhưng gắn với worksheet toán: NDBH/BTVN, CMath, các helper và thư mục không có trong dự án. Hiện thư mục skill chỉ có SKILL.md, PDF ví dụ và HTML ví dụ; các script được tham chiếu chưa tồn tại ở đây. Không chạy nguyên workflow đó cho Teacher's Guide.

Skill PPTX không cần cho đầu vào hiện tại.

## 3. Phạm vi nội dung sơ bộ từ sách

| Unit | Reading / chiến lược | Grammar | Word study | Speaking / writing |
|---|---|---|---|---|
| 1 | Bella's Home; visualizing changes | Predictions with will | Words with ei | Talking about differences; complete sentences |
| 2 | Traveling Together Around the Sun; compare and contrast in science | Future real conditional | -ance / -ant | Asking about quantity; choice questions |
| 3 | Hidden Army: Clay Soldiers of Ancient China; author's purpose | Verbs followed by infinitives | -ist | Giving reasons; verb tenses |

Vocabulary chính: 11 từ/unit, tổng 33 từ. Words in Context: 4 từ/unit, tổng 12 từ; tách khỏi nhóm chính. Các mục word study, listening và hoạt động bổ sung phải được kiểm kê riêng trước khi chốt tổng số nội dung.

## 4. Sản phẩm dự kiến

HTML local với trang tổng quan Unit 1–3, ba trang/khung ôn unit và một phần ôn trộn. Dữ liệu và ảnh tách khỏi giao diện; có bản in dễ đọc. Thông tin nguồn và đáp án nằm trong chế độ phụ huynh/giáo viên.

Mỗi unit trả lời: em đã học gì, cần nhớ gì, có thể nói/viết gì, còn cần ôn gì. Khi chưa có nhật ký lớp, dùng nhãn “nội dung trong sách”, không gắn ngày hoặc tự nhận là buổi học đã diễn ra.

Các màn hình ôn tập dự kiến:

- Nhìn lại: Big Question, hình gợi nhớ, sơ đồ gọn.
- Nhớ từ: ảnh sách + từ + nghe + IPA + sound-it-out; nghĩa tiếng Anh ngắn, tiếng Việt mở khi cần.
- Nhớ bài đọc: nhân vật/ý chính hoặc thông tin cốt lõi; câu hỏi bám nguồn và dấu vết bằng chứng.
- Dùng tiếng Anh: grammar trong ngữ cảnh, ví dụ mẫu và một câu tự tạo.
- Tự kể lại: lựa chọn nói, viết hoặc vẽ + giải thích.
- Kiểm tra nhớ: ẩn từ, nhìn ảnh gọi tên, chọn/sắp xếp, hoàn thành câu và retell ngắn.

Khuyến nghị thiết kế ban đầu: lượt ôn 10–15 phút, hoạt động 2–4 phút, một yêu cầu chính mỗi màn hình, 4–6 thẻ trong một lượt ôn. Đây là tham số thử nghiệm cần điều chỉnh theo mức ESL thực tế, không phải chuẩn tuổi bắt buộc. Không suy trình độ CEFR từ Grade 4.

## 5. Các giai đoạn triển khai

### A — Audit và mô hình hóa nguồn

1. Xác nhận ranh giới các trang Unit 1–3 bằng nội dung, không chỉ dựa vào offset mục lục.
2. Trích text theo vùng và render các trang cần đối chiếu; chỉ OCR vùng thiếu/hỏng text. Không render toàn bộ 232 trang ở độ phân giải cao mặc định.
3. Lập content matrix: unit, lesson strand, mục tiêu, vocabulary, grammar, reading, listening, speaking, writing, word study, nguồn trang.
4. Tách student content, teacher guidance và answer key. Đánh dấu uncertain để đối chiếu thay vì tự điền.
5. Nếu có nhật ký lớp sau này, thêm session_id, ngày học và trạng thái đã học; không làm lại lớp trích nguồn.

Đầu ra: source manifest + content matrix + danh sách nội dung chưa xác minh.

### B — Trích và đối chiếu ảnh sách

1. Lập inventory ảnh theo từ. Ưu tiên đúng ảnh ở bài Words; với Unit 2 khảo sát reading/exercises và phần còn lại của unit.
2. Dùng embedded image nếu hoàn chỉnh; nếu ảnh là một phần trong ảnh trang lớn, vector hoặc composite, crop trực tiếp vùng PDF bằng PyMuPDF ở độ phân giải phù hợp.
3. Lưu crop bằng tọa độ PDF và ghi rõ hệ tọa độ; giữ bản nguồn đối chiếu. Không dùng ảnh chụp màn hình HTML làm nguồn.
4. Tách nhãn từ khỏi ảnh để recall mode thực sự kiểm tra nhớ. Khi nhãn/chi tiết là phần thiết yếu của sơ đồ, giữ nguyên và ghi nhận giới hạn của câu hỏi recall.
5. Không kéo giãn ảnh nhỏ hoặc xén mất dấu hiệu phân biệt nghĩa. Một ảnh có thể hỗ trợ nhiều từ nếu có quan hệ rõ ràng; không coi mọi vật thể trong cảnh là ảnh đúng cho mọi từ.
6. Trạng thái mỗi từ: exact-book-image / supporting-book-image / no-suitable-book-image / needs-review. Thiếu ảnh phải hiển thị trung thực; sơ đồ tự tạo chỉ là hỗ trợ có nhãn riêng, không được ghi là ảnh sách.

Metadata dự kiến: vocab_id, source_file, pdf_page_1based, printed_teacher_page, student_book_page, bbox_pdf_points, extraction_method, asset_path, alt, visual_role, match_status, review_status.

Đầu ra: assets/images + image manifest + bảng coverage. Unit 1 và 3 đặt mục tiêu 11/11 ảnh đúng theo trang đã kiểm tra; Unit 2 chỉ chốt coverage sau audit.

### C — Nâng cấp skill

- Thêm mode `unit-review` và `multi-unit-review` vào skill ESL; giữ mode bài học mới.
- Đưa workflow tổng kết, mô hình dữ liệu và quy tắc ảnh vào references/schema riêng, liên kết từ SKILL.md.
- Mở rộng vocabulary schema, không thay đổi các trường IPA/sound_out/voice đang dùng nếu tương thích.
- Thêm prompt mẫu tổng kết Unit 1–3, output contract và QA riêng cho review.
- Bổ sung helper trích PDF/crop có thể chạy độc lập trong dự án; loại sự phụ thuộc vào script toán trong luồng ESL. Chỉ sửa skill OCR dùng chung khi thực sự cần, tránh áp quy tắc ESL lên worksheet toán.

Đầu ra: skill đã cập nhật + references/schema + script và prompt sử dụng được.

### D — Pilot Unit 1

Làm một lát cắt hoàn chỉnh: 11 vocab có ảnh sách, phát âm, một phần đọc, will, sơ đồ, recall và bản in. Pilot giải quyết chất lượng crop thực tế, độ dài nội dung và thao tác của trẻ trước khi nhân rộng.

Đầu ra: Unit 1 chạy được, báo cáo QA và các giới hạn có bằng chứng.

### E — Hoàn thành Unit 2–3 và ôn trộn

Nhân rộng cấu trúc đã ổn định; điều chỉnh hoạt động theo chiến lược đọc từng unit. Ôn trộn dùng nội dung đã học, không thêm Unit 4. Giữ hai nhánh chủ đề space/history trên trang tổng quan, không ép thành một sơ đồ quan hệ giả.

Đầu ra: HTML Unit 1–3, dữ liệu nguồn, toàn bộ asset, answer key và bản in.

### F — Kiểm tra trước bàn giao

- Đủ 33 từ chính và 12 từ ngữ cảnh theo source matrix; kiểm kê word study riêng, không lẫn nhóm.
- Đúng grammar, reading strategy, speaking/writing và ranh giới Unit 3.
- Mọi nội dung cốt lõi có trang nguồn; mọi asset sách có vị trí nguồn và đối chiếu ảnh–nghĩa.
- Không lộ teacher answers trong màn hình recall; không báo thành công nếu ảnh thiếu hoặc không đúng từ.
- IPA, stress, sound-it-out được đối chiếu nhất quán; audio đọc đúng từ/cụm đích, không đọc headword gần giống. TTS không được ghi là audio chính thức của sách. Listening scripts từ sách có thể dùng làm nguồn; thiếu file audio chính thức phải được ghi rõ.
- Kiểm tra ảnh, đọc và thao tác trên desktop/mobile; nút dễ bấm, bàn phím dùng được, không phụ thuộc hover; bản in không bị cắt ảnh/chữ.
- Đường dẫn asset tồn tại; local mở đúng; JS không lỗi; kiểm tra fallback audio trong điều kiện thực tế. Không hứa offline cho API/TTS khi chưa kiểm chứng.
- QA rubric hiện có đạt ngưỡng; bổ sung gate ảnh và phạm vi review. Điểm tổng không bù được sai nội dung sách hoặc sai hình.

## 6. Thứ tự ưu tiên

P0: source matrix chính xác + ảnh sách + chế độ review phù hợp trẻ + giữ hỗ trợ phát âm.

P1: sơ đồ recall, nói/viết có gợi ý, ôn trộn, bản in và ghi nhớ tiến độ đơn giản.

P2: mở rộng ngoài sách, dịch vụ ngoài, dashboard phức tạp. Chưa cần trong đợt này.

Thông tin cần để làm đúng nghĩa “tổng kết từng buổi” là nhật ký/phạm vi thực tế của lớp. Trong khi chưa có, triển khai bản tổng kết theo Unit 1–3 từ sách; các buổi ôn đề xuất phải được ghi là đề xuất.

## 7. QA và validation bắt buộc theo từng giai đoạn

Đây là thiết kế kiểm tra cho đợt triển khai. Bản xem thử đã chạy 271 kiểm tra dữ liệu và 108 kiểm tra trình duyệt; kết quả và bằng chứng nằm tại [qa/QA_REPORT.md](qa/QA_REPORT.md). Các kiểm tra chưa thực hiện, gồm quan sát học sinh và nghe voice trên thiết bị của bé, được đánh dấu rõ trong báo cáo.

| Điểm kiểm tra | Cách validate | Điều kiện pass | Bằng chứng lưu |
|---|---|---|---|
| Sau A: nguồn | Đối chiếu content matrix với Scope and Sequence và trang bài học; kiểm tra trực quan vùng student/teacher/answer | Đủ mục trong phạm vi Unit 1–3; không lẫn Unit 4; mọi mục có nguồn; điểm chưa rõ được đánh dấu | source-audit.md và content matrix |
| Sau B: ảnh | Script kiểm tra manifest, file tồn tại, bbox trong trang, kích thước hợp lệ; xem contact sheet và đối chiếu từng ảnh với trang sách | Không có ảnh sai từ, crop mất chi tiết hoặc nhãn rò đáp án; mọi từ có trạng thái coverage trung thực | image-manifest.json, contact sheet, image-review.md |
| Sau C: cấu trúc skill | Chạy quick_validate.py của skill-creator; kiểm tra toàn bộ reference và helper được nhắc đến | Frontmatter hợp lệ; không có placeholder chưa xử lý; link/script đúng và có thật | skill-validation.md với lệnh và kết quả |
| Sau C: hành vi skill | Dùng các tình huống: review một unit, review Unit 1–3, thiếu ảnh Unit 2, thiếu nhật ký lớp, text OCR lỗi; đánh giá đầu ra với raw source | Chọn đúng review mode; không tự bịa buổi học/ảnh/nội dung; giữ đối tượng 9 tuổi ESL; báo thiếu dữ liệu rõ ràng | behavioral-validation.md và đầu ra từng tình huống |
| Sau D: pilot Unit 1 | Kiểm tra toàn bộ 11 thẻ; dùng thử đọc → grammar → diễn đạt → recall; kiểm tra audio, reload, mobile và print | Không còn lỗi chặn học; ảnh đúng sách; phát âm đúng mục tiêu; recall không lộ đáp án; rubric đạt yêu cầu | pilot-qa.md, ảnh chụp giao diện và bảng lỗi |
| Sau E–F: sản phẩm đầy đủ | Validate dữ liệu và asset bằng script; kiểm tra nội dung toàn bộ ba unit; smoke test các luồng tương tác và fallback audio | Đủ nội dung đã chốt; không lỗi JS/path; các luồng chính hoạt động; mọi giới hạn được báo đúng | final-qa.md, kết quả kiểm tra và bảng coverage |

### QA sư phạm dành riêng cho học sinh 9 tuổi ESL

- Mỗi màn hình có nhiệm vụ rõ ràng, hướng dẫn ngắn và ví dụ/gợi ý khi cần; không đưa jargon hoặc teacher notes vào Child Mode.
- Định nghĩa và câu mẫu dùng ngôn ngữ dễ tiếp cận, nhưng giữ đúng nghĩa từ trong bài. Grade 4 không được dùng thay cho đánh giá mức ESL.
- Hoạt động phân biệt nhận biết, nhớ lại và dùng được: chọn ảnh đúng chưa đủ để kết luận em nói/viết được từ.
- Câu hỏi đọc hiểu có đáp án hoặc tiêu chí chấp nhận bám nguồn; câu hỏi mở không ép một đáp án duy nhất.
- Grammar ôn đúng cấu trúc từng unit và có nhiệm vụ dùng trong ngữ cảnh.
- Kiểm tra quan hệ trên sơ đồ; không để thiết kế đẹp che đi quan hệ sai.
- Review chuyên môn có thể xác nhận scaffold phù hợp dự kiến. Khả năng trẻ tự dùng và thời lượng thực tế chỉ được xác nhận sau khi có quan sát học sinh; nếu chưa có, ghi là chưa kiểm chứng với học sinh.

### Phân loại lỗi và quy tắc bàn giao

- **Blocker:** sai phạm vi/nội dung sách; ảnh sai nghĩa; audio sai từ; đáp án lộ trong recall; luồng chính không dùng được. Phải sửa trước khi bàn giao.
- **Major:** hướng dẫn khó hiểu, thiếu scaffold cần thiết, chữ/ảnh khó đọc, fallback không đúng mô tả. Phải sửa trước khi tuyên bố hoàn thành.
- **Minor:** lỗi trình bày nhỏ không làm sai nghĩa hoặc cản thao tác. Ghi vào báo cáo nếu còn.
- Ảnh Unit 2 chưa có hoặc audio chính thức chưa được cung cấp là giới hạn đầu vào khi đã được ghi rõ và có cách học phù hợp; không được che bằng ảnh/audio gắn nhãn sai.
- Chỉ nhân rộng sau khi pilot Unit 1 qua gate. Sau sửa lỗi, chạy lại kiểm tra bị ảnh hưởng và các luồng phụ thuộc.
- Báo cáo mỗi check bằng PASS / FAIL / NOT RUN / BLOCKED kèm bằng chứng. Không dùng điểm rubric tổng để bỏ qua blocker hoặc major.
- Validate cấu trúc skill không thay thế behavioral validation; QA bằng người lớn không thay thế quan sát trẻ sử dụng.
