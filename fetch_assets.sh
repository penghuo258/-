#!/usr/bin/env bash
# 补齐原站 PC 高清资源（srcset 中的桌面版变体）
set -u
cd "$(dirname "$0")/original/assets" || exit 1
BASE="https://revenants-of-azvaldt.shadowverse-wb.com/_app/immutable/assets"

FILES="bg_movie.cEpslkXM.webp bg_story.CMxUj60d.webp catch.tPrU7Ulz.webp
chara0_img1.CkcwMNk-.webp chara1_img1.CmpVLriE.webp chara1_img2.0RAzhhvv.webp
chara2_img1.47LmPJRS.webp chara2_img2.y5kokwJy.webp chara3_img1.DOpAq8aR.webp
chara4_img1.bdPXiO2k.webp chara4_img2._wNtJtA1.webp chara5_img1.D1USSWK9.webp
chara5_img2.DI9gGt7X.webp chara6_img1.sGdlM3gY.webp chara6_img2.BRphVI6r.webp
chara7_img1.DaOo39Z_.webp chara7_img2.CYOefJdm.webp chara8_img1.SbYqNDrw.webp
chara_btn_bishop.D05WCtFY.webp chara_btn_dragon.DhRBbY8v.webp
chara_btn_elf.BumFol0-.webp chara_btn_nemesis.Dj0saUg_.webp
chara_btn_neutral.B_CFxn4T.webp chara_btn_neutral.DwyLiVfj.webp
chara_btn_nightmare.BFewCEBa.webp chara_btn_royal.CUPv4DCs.webp
chara_btn_witch.B30-WcHh.webp chara_profile_bishop.Biz6hQen.webp
chara_profile_dragon.BJy6oJoV.webp chara_profile_elf.C54BIMOR.webp
chara_profile_nemesis.CAS0rmih.webp chara_profile_neutral.BHc-nmGW.webp
chara_profile_neutral.D7Z-TYWy.webp chara_profile_nightmare.B2ZjrMkw.webp
chara_profile_royal.EHl47FN9.webp chara_profile_witch.Cqpk0uNH.webp
chara_voice.CRMOMoGV.svg chara_zoom.BUsMGhp_.svg
floor0.BO9tIXFh.webp floor1.CiIc2B55.webp floor2.DgshzFmB.webp
floor3.BC_oinE8.webp floor4.mU9H_v5c.webp floor5.W5xEVwea.webp
floor6.CshQGd_U.webp floor7.cNtys-FB.webp floor8.BcId6Rpx.webp
footer_btn_img.cdxNyVyA.webp footer_btn_logo.BILZ_Trr.webp
kv_btn1_items.BWpxFgHT.webp kv_btn1_items.Diqlby_N.webp
kv_logo.EXrzYxVI.webp kv_logo_svwb.tpquFVW7.webp
kv_pv_thumb1.D1y1h9vx.webp kv_pv_thumb2.87S_YyPV.webp
kv_pv_ttl1.CO-95Drv.svg kv_pv_ttl1.D-6fN4Up.svg
kv_pv_ttl2.C3OrUzAv.svg kv_pv_ttl2.yo_8wthj.svg"

fail=0
for f in $FILES; do
  if [ -s "$f" ]; then continue; fi
  if ! curl -sS -f --max-time 25 -o "$f" "$BASE/$f"; then
    echo "FAIL $f"
    rm -f "$f"
    fail=$((fail+1))
  fi
done
echo "=== 完成，失败 $fail 个；目录共 $(ls | wc -l) 个文件"